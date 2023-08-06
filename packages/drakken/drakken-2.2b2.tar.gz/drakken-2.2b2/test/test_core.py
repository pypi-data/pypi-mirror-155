import unittest

import requests
from wsgiadapter import WSGIAdapter  # from requests-wsgi-adapter

from drakken.core import Drakken, Blueprint
from drakken.exceptions import redirect


class TestCore(unittest.TestCase):
    def setUp(self):
        self.app = Drakken()
        self.client = requests.Session()
        self.client.mount(
            prefix='http://testserver',
            adapter=WSGIAdapter(
                self.app))

    def test_blueprint(self):
        s = 'Calm, steamy morning.'
        bp = Blueprint(name='accounts', url_prefix='/customer-account')

        @bp.route('/home')
        def home(request, response):
            response.text = s

        self.app.register_blueprint(bp)
        url = 'http://testserver/customer-account/home'
        self.assertTrue(self.client.get(url).text == s)

    def test_redirect(self):

        @self.app.route('/foo')
        def foo(request, response):
            response.text = 'Foo'
            redirect('/bar')

        @self.app.route('/bar')
        def bar(request, response):
            response.text = 'Bar'

        response = self.client.get(
            'http://testserver/foo',
            allow_redirects=True)
        self.assertEqual(response.text, 'Bar')


if __name__ == '__main__':
    unittest.main()

