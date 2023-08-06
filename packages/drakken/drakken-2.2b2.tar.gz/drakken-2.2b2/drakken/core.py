"""Routing module."""
import inspect
import io
import mimetypes
import os

from parse import parse
import webob

from .config import config
from .exceptions import BadRequest, LoginFail, NotFound, HTTPRedirect
from .middleware import Middleware
from .templates import render

TEXT_FILE_TYPES = [
    'text/css',
    'text/csv',
    'text/html',
    'text/calendar',
    'application/javascript',
    'text/javascript',
    'text/plain',
    'text/xml']


class Drakken:
    """The Drakken App class."""

    def __init__(self):
        self.routes = {}
        # Middleware wraps around self (the application).
        self.middleware = Middleware(self)

    def __call__(self, environ, start_response):
        """WSGI API.

        Args:
            environ: dictionary of environment variables.
            start_response: callback function sending HTTP status and
            headers to server.
        """
        return self.middleware(environ, start_response)

    def add_middleware(self, middleware):
        """Add middleware.

        Args:
            middleware: subclass of drakken.middleware.Middleware.
        """
        self.middleware.add(middleware)

    def _handle_static_file(self, request, response):
        """Serve static file if in development.

        In production the web server will intercept the request before
        it gets to the app so development-only logic is unnecessary.
        """
        fpath = os.path.join(os.getcwd(), request.path[1:])
        if os.path.exists(fpath):
            ftype = mimetypes.guess_type(fpath)[0]
            response.content_type = ftype
            if ftype in TEXT_FILE_TYPES:
                with io.open(fpath, 'r', encoding='ISO-8859-1') as f:
                    response.text = f.read()
            else:
                with io.open(fpath, 'rb') as f:
                    response.body = f.read()
            return response
        else:
            self._not_found(response)

    def _not_allowed(self, response):
        response.status_code = 400
        response.text = 'Not allowed.'

    def _not_found(self, response):
        response.status_code = 404
        template_path = os.path.join(
            config['TEMPLATE_DIR'],
            '404.html')
        if os.path.exists(template_path):
            response.text = render(response, '404.html')
        else:
            response.text = 'Not found.'

    def _find_handler(self, path):
        """Find the request handler for this request path.

        Args:
            path: URL path string.
        """
        for request_path, handler in self.routes.items():
            parse_result = parse(request_path, path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def handle_request(self, request):
        """Find and execute the handler for this request.

        Args:
            request: WebOb.Request object.
        """
        response = webob.Response()
        try:
            handler, kwargs = self._find_handler(path=request.path)
        except UnicodeDecodeError:
            response.status_code = 400
            response.text = 'Bad Request'
            return response
        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    # If request.method (POST, GET, PUT, DELETE) isn't
                    # implemented in the request handler, return 400.
                    self._not_allowed(response)
                    return response
            try:
                handler(request, response, **kwargs)
            except BadRequest:
                response.status_code = 400
                response.text = 'Bad Request'
            except HTTPRedirect as exc:
                response.status_code = exc.status_code
                response.location = exc.path
            except LoginFail:
                response.status_code = 401
                response.text = 'Unauthorized'
            except NotFound:
                self._not_found(response)
        elif request.path.startswith(
                os.path.join('/', config['STATIC_DIR'])):
            self._handle_static_file(request, response)
        else:
            # Default handler: 404 not found.
            self._not_found(response)
        return response

    def register_blueprint(self, blueprint):
        """Store blueprint.

        Args:
            blueprint: a drakken.core.Blueprint object.
        """
        for route, handler in blueprint.routes.items():
            path = f'{blueprint.url_prefix}{route}'.replace('//', '/')
            # TODO: might need to use a SimpleNamespace to hold blueprint
            # options.
            self.routes[path] = handler

    def route(self, path):
        """Decorator to store route.

        Args:
            path: an URL path string.
        """
        if path in self.routes:
            raise AssertionError('Route already exists.')

        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper

    def runserver(self):
        """Run development server forever."""
        from wsgiref.simple_server import make_server
        with make_server('', 8000, self) as httpd:
            print('Starting development server at http://127.0.0.1:8000')
            print('Quit the server with CONTROL-C.')
            httpd.serve_forever()


class Blueprint(object):
    """A container for storing related page handlers.

    Allows you to divide an app into logical components: an accounts
    blueprint, a documents blueprint, etc.
    """

    def __init__(self, name, url_prefix=''):
        """Initialize.

        Args:
            name: blueprint name string.
            url_prefix: URL prefix string.
        """
        self.name = name
        self.url_prefix = url_prefix
        self.routes = {}

    def route(self, path):
        """Add URL path to blueprint.

        Args:
            path: URL path string.

        Use as a decorator.

        Raises:
            AssertionError: If the route already exists in the blueprint.
        """
        if path in self.routes:
            raise AssertionError('Route already exists.')

        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper

