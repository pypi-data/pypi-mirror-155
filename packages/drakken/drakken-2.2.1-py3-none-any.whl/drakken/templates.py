"""Template module."""
import os
from types import SimpleNamespace

from mako.template import Template
from mako.lookup import TemplateLookup
import sqlalchemy

from .config import config
from .exceptions import LoginFail
import drakken.model as model
import drakken.security as security


def create_CSRF_input(csrf_token, ip_address, user_agent):
    """Create CSRF token and store in session table.

    Args:
        csrf_token: CSRF token string.
        ip_address: request IP address string.
        user_agent: request user agent string.

    Returns:
        CSRF token string.
    """
    if not csrf_token:
        csrf_token = security.create_CSRF_token()
        with model.session_scope() as sql_session:
            session = model.Session(
                csrf_token=csrf_token,
                ip_address=ip_address,
                user_agent=user_agent)
            sql_session.add(session)
    return csrf_token


def render(request, template, context={}):
    """Render template and return as string.

    Args:
        request: WebOb.Request object.
        template: path string to template in config.TEMPLATE_DIR.
        context: dictionary of objects to load into template.

    Returns:
        HTML rendered from template.
    """
    try:
        session = model.get_session(request)
        user = session.user
        csrf_token = session.csrf_token
    except (LoginFail, sqlalchemy.exc.UnboundExecutionError):
        # No db connection detected. Allows Drakken to be used without a db.
        user = SimpleNamespace(is_authenticated=False)
        csrf_token = None
    context['user'] = user
    path = os.path.join(config['TEMPLATE_DIR'], template)
    lookup = TemplateLookup(directories=[os.getcwd()])
    t = Template(filename=path, lookup=lookup)
    context['STATIC'] = config['STATIC_DIR']
    # Generate CSRF token only if called for in template.
    if '${CSRF}' in t.source:
        context['CSRF'] = create_CSRF_input(
            csrf_token=csrf_token,
            ip_address=request.client_addr,
            user_agent=request.user_agent)
    return t.render(**context)


def read(path):
    """Read text file and return string.

    Args:
        path: file path string from config.TEMPLATE_DIR.

    Returns:
       String contents of file.
    """
    path = os.path.join(config['TEMPLATE_DIR'], path)
    with open(path, 'r') as f:
        s = f.read()
    return s

