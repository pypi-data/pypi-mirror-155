import unittest

import drakken.security as security


class TestSecurity(unittest.TestCase):
    def test_create_cookie(self):
        token = security.create_session_token()
        cookie = security.create_session_cookie(token)
        self.assertEqual(cookie['name'], 'sessionid')
        self.assertEqual(cookie['secure'], False)
        self.assertEqual(cookie['httponly'], True)
        self.assertEqual(cookie['samesite'], 'strict')

    def test_create_session_token(self):
        token = security.create_session_token()
        self.assertTrue(len(token) >= 16)

    def test_create_CSRF_token(self):
        token = security.create_CSRF_token()
        self.assertTrue(len(token) > 16)

    def test_fast_hash(self):
        s = 'hello world'
        hashed = security.fast_hash(s)
        self.assertTrue(s != hashed)

    def test_hash(self):
        s = 'hello world'
        salt = security.gensalt()
        hashed = security.slow_hash(s, salt)
        self.assertTrue(security.verify(s, salt, hashed))


if __name__ == '__main__':
    unittest.main()

