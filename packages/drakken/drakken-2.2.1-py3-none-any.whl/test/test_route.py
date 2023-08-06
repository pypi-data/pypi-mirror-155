import unittest

import requests
from wsgiadapter import WSGIAdapter  # from requests-wsgi-adapter

from drakken.core import Drakken
from drakken.exceptions import BadRequest, NotFound


class TestRoute(unittest.TestCase):
    def setUp(self):
        self.app = Drakken()
        self.client = requests.Session()
        self.client.mount(
            prefix='http://testserver',
            adapter=WSGIAdapter(
                self.app))

    def test_basic_route(self):
        s = 'Calm, steamy morning.'

        @self.app.route('/home')
        def home(request, response):
            response.text = s

        self.assertTrue(
            self.client.get('http://testserver/home').text == s)

    def test_duplicate_route(self):

        @self.app.route('/home')
        def home(request, response):
            response.text = 'Home page'

        self.assertTrue(self.app.routes['/home'] is home)

        with self.assertRaises(AssertionError):
            @self.app.route('/home')
            def second_home(request, response):
                response.text = 'Second home page'

    def test_hacker_intrusion(self):

        @self.app.route('/')
        @self.app.route('/home')
        def home(request, response):
            response.text = 'Home page'

        url = 'http://testserver/%ff'
        self.assertEqual(self.client.get(url).status_code, 400)


if __name__ == '__main__':
    unittest.main()

