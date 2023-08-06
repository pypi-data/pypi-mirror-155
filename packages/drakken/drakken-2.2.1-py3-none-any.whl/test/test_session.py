from datetime import date, timedelta
from importlib import reload
import random
import string
import unittest

from drakken.config import read_dict
import drakken.exceptions as exception
import drakken.model as model
import drakken.security as security


cfg = {
    'DATABASE_URL': 'sqlite:///:memory:',
    'SESSION_COOKIE_AGE': 1209600,
}
read_dict(cfg)


class MockRequest:
    def __init__(self, token):
        self.POST = {}
        self.POST['CSRFToken'] = token
        self.user_agent = 'My Web Browser'
        self.client_addr = 'Mock Request'
        self.environ = {}
        self.cookies = {}


class MockResponse:
    def __init__(self):
        self.cookies = {}

    def set_cookie(self, *args, **kwargs):
        self.cookies = kwargs


def srandom(length=32):
    """Return random string."""
    return ''.join([random.choice(string.ascii_lowercase)
                    for i in range(length)])


class TestCreateUser(unittest.TestCase):
    def setUp(self):
        model.setup()

    def test_create_user(self):
        email = 'stuart@erewhon.com'
        password = 'Found in the swamp'
        model.create_user(email, password)
        with model.session_scope() as session:
            user = session.query(
                model.User).filter_by(email=email).first()
            self.assertEqual(user.email, email)
            self.assertTrue(security.verify(password, user.salt, user.pwhash))

    def test_create_user_email_taken(self):
        email = 'stuart@erewhon.com'
        password = 'Found in the swamp'
        model.create_user(email, password)
        with self.assertRaises(exception.EmailAddressTaken):
            model.create_user(email, password)

    def test_create_user_short_password(self):
        # Per OWASP: min password length 8.
        email = 'stuart@erewhon.com'
        password = 'wee'
        with self.assertRaises(exception.PasswordLength):
            model.create_user(email, password)

    def test_create_user_long_password(self):
        # Per OWASP: set max password length to prevent password DOS attacks.
        email = 'stuart@erewhon.com'
        password = srandom(length=80)
        with self.assertRaises(exception.PasswordLength):
            model.create_user(email, password)

    def test_username(self):
        d = dict(USERNAME=True)
        read_dict(d)
        reload(model)
        model.setup()
        username = 'Stuart'
        email = 'stuart@erewhon.com'
        password = 'Found in the swamp'
        model.create_user(email, password, username)
        with model.session_scope() as session:
            user = session.query(
                model.User).filter_by(username=username).first()
            self.assertEqual(user.email, email)
            self.assertTrue(security.verify(password, user.salt, user.pwhash))

    def test_username_taken(self):
        d = dict(USERNAME=True)
        read_dict(d)
        reload(model)
        model.setup()
        username = 'Stuart'
        email = 'stuart@erewhon.com'
        password = 'Found in the swamp'
        model.create_user(email, password, username)
        with self.assertRaises(exception.UserNameTaken):
            model.create_user(email, password, username)

    def tearDown(self):
        d = dict(USERNAME=False)
        read_dict(d)
        reload(model)


class TestAuthenticate(unittest.TestCase):
    def setUp(self):
        model.setup()
        self.email = 'stuart@erewhon.com'
        self.password = 'Found in the swamp'
        model.create_user(self.email, self.password)

    def test_authenticate_password_mismatch(self):
        with self.assertRaises(exception.AuthenticateFail):
            model.authenticate(email=self.email, password='bad-password')

    def test_authenticate_email_not_found(self):
        with self.assertRaises(exception.AuthenticateFail):
            model.authenticate(email='bad-email', password=self.password)


class TestEmailLogin(unittest.TestCase):
    def setUp(self):
        model.setup()
        self.email = 'stuart@erewhon.com'
        self.password = 'Found in the swamp'
        model.create_user(self.email, self.password)

        # Login must require CSRF token to prevent session fixation attacks
        # per OWASP.
        self.csrf_token = security.create_CSRF_token()
        # Store token in database
        with model.session_scope() as sql_session:
            user = sql_session.query(model.User).first()
            session = model.Session(
                csrf_token=self.csrf_token,
                user_agent='My Web Browser')
            sql_session.add(session)

    def test_login_logout(self):
        request = MockRequest(self.csrf_token)
        response = MockResponse()
        model.login(
            email=self.email, password=self.password,
            request=request, response=response)
        sessionid = response.cookies.get('value')

        # Verify logged in.
        with model.session_scope() as session:
            login_session = session.query(model.Session).first()
            self.assertEqual(
                login_session.session_token,
                security.fast_hash(sessionid))

        # Logout user
        request = MockRequest(self.csrf_token)
        request.cookies['sessionid'] = sessionid
        response = MockResponse()
        model.logout(request, response)

        # Verify session deleted
        with model.session_scope() as session:
            count = session.query(model.Session).count()
            self.assertEqual(count, 0)

    def test_user_agent_mismatch(self):
        # Login user
        request = MockRequest(self.csrf_token)
        response = MockResponse()
        model.login(
            email=self.email, password=self.password,
            request=request, response=response)
        sessionid = response.cookies.get('value')

        request = MockRequest(self.csrf_token)
        request.cookies['sessionid'] = sessionid
        request.user_agent = 'bad-user-agent'

        with self.assertRaises(exception.LoginFail):
            model.get_session(request)

    def test_session_expired(self):
        # Sessions expire after 2 weeks.
        one_year_ago = date.today() - timedelta(days=365)
        one_week_ago = date.today() - timedelta(days=7)

        # Login user
        request = MockRequest(self.csrf_token)
        response = MockResponse()
        model.login(
            email=self.email, password=self.password,
            request=request, response=response)
        sessionid = response.cookies.get('value')

        # Set session date to 1 week ago - should login.
        with model.session_scope() as session:
            sid = session.query(model.Session).first()
            sid.date_created = one_week_ago

        # Call get_session() - should authenticate.
        request = MockRequest(self.csrf_token)
        request.cookies['sessionid'] = sessionid
        record = model.get_session(request)
        self.assertTrue(record.user.is_authenticated)

        # Set session date to 1 year ago - should fail login.
        with model.session_scope() as session:
            sid = session.query(model.Session).first()
            sid.date_created = one_year_ago

        with self.assertRaises(exception.LoginFail):
            model.get_session(request)

    def test_inactive_user_session(self):
        # Login user
        request = MockRequest(self.csrf_token)
        response = MockResponse()
        model.login(
            email=self.email, password=self.password,
            request=request, response=response)
        sessionid = response.cookies.get('value')

        with model.session_scope() as sql_session:
            user = sql_session.query(model.User).first()
            user.active = False

        request = MockRequest(self.csrf_token)
        request.cookies['sessionid'] = sessionid
        request.user_agent = 'My Web Browser'

        with self.assertRaises(exception.AccountDisabled):
            model.get_session(request)

    def test_inactive_user_login(self):
        with model.session_scope() as sql_session:
            user = sql_session.query(model.User).first()
            user.active = False

        request = MockRequest(self.csrf_token)
        response = MockResponse()
        with self.assertRaises(exception.AccountDisabled):
            model.login(
                email=self.email, password=self.password,
                request=request, response=response)


class TestUserNameLogin(unittest.TestCase):
    def setUp(self):
        d = dict(USERNAME=True)
        read_dict(d)
        reload(model)
        model.setup()
        self.username = 'Stuart'
        self.email = 'stuart@erewhon.com'
        self.password = 'Found in the swamp'
        model.create_user(self.email, self.password, self.username)

        # Login must require CSRF token to prevent session fixation attacks
        # per OWASP.
        self.csrf_token = security.create_CSRF_token()
        # Store token in database
        with model.session_scope() as sql_session:
            user = sql_session.query(model.User).first()
            session = model.Session(
                csrf_token=self.csrf_token,
                user_agent='My Web Browser')
            sql_session.add(session)

    def test_login_logout(self):
        request = MockRequest(self.csrf_token)
        response = MockResponse()
        model.login(
            username=self.username, password=self.password,
            request=request, response=response)
        sessionid = response.cookies.get('value')

        # Verify logged in.
        with model.session_scope() as session:
            login_session = session.query(model.Session).first()
            self.assertEqual(
                login_session.session_token,
                security.fast_hash(sessionid))

        # Logout user
        request = MockRequest(self.csrf_token)
        request.cookies['sessionid'] = sessionid
        response = MockResponse()
        model.logout(request, response)

        # Verify session deleted
        with model.session_scope() as session:
            count = session.query(model.Session).count()
            self.assertEqual(count, 0)

    def tearDown(self):
        d = dict(USERNAME=False)
        read_dict(d)
        reload(model)


class TestMisc(unittest.TestCase):
    def setUp(self):
        model.setup()
        self.email = 'stuart@erewhon.com'
        self.password = 'Found in the swamp'
        model.create_user(self.email, self.password)

    def test_change_password(self):
        with model.session_scope() as session:
            user = session.query(model.User).first()

        pw = srandom()
        model.update_password(user.id, pw)

        with model.session_scope() as session:
            user = session.query(model.User).first()
            self.assertTrue(security.verify(pw, user.salt, user.pwhash))

    def test_validate_CSRF(self):
        csrf_token = security.create_CSRF_token()

        # Store token in database
        with model.session_scope() as sql_session:
            user = sql_session.query(model.User).first()
            session = model.Session(
                csrf_token=csrf_token,
                user_agent='My Web Browser',
                user=user)
            sql_session.add(session)

        request = MockRequest(csrf_token)
        self.assertTrue(model.validate_CSRF(request))

        with self.assertRaises(exception.CSRFTokenFail):
            model.validate_CSRF(MockRequest('bad-token'))


class TestLoginRequired(unittest.TestCase):
    def setUp(self):
        model.setup()
        self.email = 'stuart@erewhon.com'
        self.password = 'Found in the swamp'
        model.create_user(self.email, self.password)

        # Store CSRF token
        self.csrf_token = security.create_CSRF_token()
        with model.session_scope() as sql_session:
            user = sql_session.query(model.User).first()
            session = model.Session(
                csrf_token=self.csrf_token,
                user_agent='My Web Browser')
            sql_session.add(session)

        # Login user
        request = MockRequest(self.csrf_token)
        response = MockResponse()
        model.login(
            email=self.email, password=self.password,
            request=request, response=response)
        self.sessionid = response.cookies.get('value')

    def test_logged_in(self):

        @model.login_required
        def foo(request, response):
            return 'hello'

        request = MockRequest(self.csrf_token)
        request.cookies['sessionid'] = self.sessionid
        response = MockResponse()
        self.assertEqual(foo(request, response), 'hello')

    def test_logged_out(self):

        @model.login_required
        def foo(request, response):
            return 'hello'

        request = MockRequest(self.csrf_token)
        request.cookies['sessionid'] = ''
        response = MockResponse()
        with self.assertRaises(exception.LoginFail):
            foo(request, response)

    def test_redirect_implied(self):
        # The default for Redirect = True.

        cfg['LOGIN_URL'] = 'my-login-url'
        read_dict(cfg)

        @model.login_required
        def foo(request, response):
            return 'hello'

        request = MockRequest(self.csrf_token)
        request.cookies['sessionid'] = ''
        response = MockResponse()
        with self.assertRaises(exception.HTTPRedirect):
            foo(request, response)

    def test_redirect_true(self):
        cfg['LOGIN_URL'] = 'my-login-url'
        read_dict(cfg)

        @model.login_required(redirect=True)
        def foo(request, response):
            return 'hello'

        request = MockRequest(self.csrf_token)
        request.cookies['sessionid'] = ''
        response = MockResponse()
        with self.assertRaises(exception.HTTPRedirect):
            foo(request, response)

    def test_redirect_false(self):
        cfg['LOGIN_URL'] = 'my-login-url'
        read_dict(cfg)

        @model.login_required(redirect=False)
        def foo(request, response):
            return 'hello'

        request = MockRequest(self.csrf_token)
        request.cookies['sessionid'] = ''
        response = MockResponse()
        with self.assertRaises(exception.LoginFail):
            foo(request, response)

    def tearDown(self):
        cfg['LOGIN_URL'] = ''
        read_dict(cfg)


if __name__ == '__main__':
    unittest.main()

