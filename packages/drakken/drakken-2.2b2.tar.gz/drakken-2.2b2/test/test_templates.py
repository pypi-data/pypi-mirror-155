import os
import tempfile
import unittest

import requests
from wsgiadapter import WSGIAdapter  # from requests-wsgi-adapter

from drakken.core import Drakken
import drakken.model as model
from drakken.templates import render
from drakken.config import read_dict

cfg = {
    'DATABASE_URL': 'sqlite:///:memory:',
    'TEMPLATE_DIR': '',
}
read_dict(cfg)


class TestCSRFToken(unittest.TestCase):
    def setUp(self):
        model.setup()
        self.email = 'stuart@erewhon.com'
        self.password = 'Found in the swamp'
        model.create_user(self.email, self.password)

        self.app = Drakken()
        self.client = requests.Session()
        self.client.mount(
            prefix='http://testserver',
            adapter=WSGIAdapter(
                self.app))

    def test_no_CSRF_tag_in_template(self):
        template = b'<html><p>Hello</p></html>'

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(template)
            self.template_path = f.name

        @self.app.route('/hello')
        def hello(request, response):
            response.text = render(request, self.template_path)

        user_agent = self.client.headers['User-Agent']
        headers = {'user-agent': user_agent}
        r = self.client.get(
            'http://testserver/hello',
            headers=headers)
        self.assertTrue('<p>Hello</p>' in r.text)

        with model.session_scope() as sql_session:
            count = sql_session.query(model.Session).count()
            self.assertEqual(count, 0)

    def test_not_logged_in(self):
        template = b'<html>${CSRF}</html>'

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(template)
            self.template_path = f.name

        @ self.app.route('/create-account')
        def create_account(request, response):
            response.text = render(request, self.template_path)

        user_agent = self.client.headers['User-Agent']
        headers = {'user-agent': user_agent}
        r = self.client.get(
            'http://testserver/create-account',
            headers=headers)

        with model.session_scope() as sql_session:
            token = sql_session.query(model.Session).first().csrf_token
            self.assertTrue(token in r.text)

    def tearDown(self):
        os.remove(self.template_path)


if __name__ == '__main__':
    unittest.main()

