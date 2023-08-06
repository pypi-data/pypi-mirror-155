"""ORM module.

Warning:
    SQLAlchemy doesn't escape raw SQl so to prevent SQL injection attacks
    always use the ORM.
"""
from datetime import datetime, timedelta
from functools import wraps, partial
import logging
import inspect

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, LargeBinary, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from sqlalchemy.orm import backref, relationship, sessionmaker

from .config import config
from . import exceptions
from . import security


Base = declarative_base()
SQLSession = sessionmaker(expire_on_commit=False)


class User(Base):
    """User account table."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    if config['USERNAME']:
        username = Column(String(254), unique=True)
        email = Column(String(254), unique=False)
    else:
        email = Column(String(254), unique=True)
    pwhash = Column(LargeBinary(64))
    salt = Column(String(200))
    date_joined = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)

    def __repr__(self):
        return f'<User({self.email}>'


class Session(Base):
    """Session table."""
    __tablename__ = 'sessions'
    csrf_token = Column(String(200), primary_key=True)
    date_created = Column(DateTime, default=datetime.now)
    ip_address = Column(String(32))
    session_token = Column(String(200))
    user_agent = Column(String(200))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(
        User, backref=backref(
            'sessions', cascade='all,delete'))


def create_user(email, password, username=''):
    """Create a user.

    Args:
        email: string, must be unique if not using a username.
        password: string, length must be within MIN and MAX set in config.
        username: string, must be unique.

    Note:
        The password hashing algorithm is deliberately computationally
        expensive to slow down hackers. Very long passwords can take so long
        to compute they can be used in a denial of service attack per OWASP.
        Which is why we check for too long passwords.

    Raises:
        EmailAddressTaken: If email address is already in the database.
        PasswordLength: If password is too long or too short.
        PasswordLength: If password is too long or too short.
        UserNameTaken: If user name is already in the database.
    """
    if config['USERNAME']:
        logging.info(f'{config["APP_NAME"]} create_user: {username}')
    else:
        logging.info(f'{config["APP_NAME"]} create_user: {email}')
    with session_scope() as session:
        if config['USERNAME'] and session.query(
                User).filter_by(username=username).first():
            raise exceptions.UserNameTaken
        if not config['USERNAME'] and session.query(
                User).filter_by(email=email).first():
            raise exceptions.EmailAddressTaken
        if not config['MIN_PASSWORD_LENGTH'] < len(
                password) < config['MAX_PASSWORD_LENGTH']:
            raise exceptions.PasswordLength
        salt = security.gensalt()
        hashed = security.slow_hash(password, salt)
        if config['USERNAME']:
            user = User(email=email, pwhash=hashed,
                        salt=salt, username=username)
        else:
            user = User(email=email, pwhash=hashed, salt=salt)
        session.add(user)
    return user


def authenticate(**kwargs):
    """Authenticate user.

    Args:
        email: string.
        password: string.

    Raises:
        AuthenticateFail: If username/email and password don't match the
        database.
    """
    with session_scope() as session:
        if config['USERNAME']:
            user = session.query(User).filter_by(
                username=kwargs['username']).first()
        else:
            user = session.query(User).filter_by(
                email=kwargs['email']).first()
        if not user or not security.verify(
                kwargs['password'], user.salt, user.pwhash):
            raise exceptions.AuthenticateFail


def get_session(request):
    """Return session object.

    Args:
        request: webob.Request object.

    Raises:
        LoginFail:  If session ID is missing, session ID is not in database,
            request user agent doesn't match user agent for this session, or
            session has expired.
    """
    try:
        session_token = request.cookies.get('sessionid')
        if not session_token:
            raise exceptions.LoginFail
    except Exception:
        raise exceptions.LoginFail
    user_agent = request.user_agent
    hashed_session_token = security.fast_hash(session_token)

    cookie_age = config['SESSION_COOKIE_AGE']
    with session_scope() as sql_session:
        records = sql_session.query(Session).filter(
            Session.session_token == hashed_session_token,
            Session.user_agent == user_agent)
        if cookie_age:
            # Per OWASP: set absolute session lifetime.
            earliest_date = datetime.now() - \
                timedelta(seconds=cookie_age)
            record = records.filter(
                Session.date_created >= earliest_date).first()
        else:
            record = records.first()
        if not record:
            raise exceptions.LoginFail
        if not record.user.active:
            raise exceptions.AccountDisabled
        record.user.is_authenticated = True
    return record


def login(**kwargs):
    """Login user and set response cookie.

    Args:
        username: string.
        email: string.
        password: string.
        request: webob.Request object.
        response: webob.Response object.
    """
    if config['USERNAME']:
        ident = kwargs['username']
    else:
        ident = kwargs['email']
    request = kwargs['request']
    response = kwargs['response']
    logging.info(
        f'{config["APP_NAME"]} login: {ident} ip: {request.client_addr} user agent: {request.user_agent}')
    authenticate(**kwargs)
    presession_csrf_token = validate_CSRF(request)
    with session_scope() as session:
        if config['USERNAME']:
            user = session.query(User).filter_by(username=ident).first()
        else:
            user = session.query(User).filter_by(email=ident).first()
        presession_record = session.query(Session).filter_by(
            csrf_token=presession_csrf_token).first()
        if not presession_record or presession_record.user:
            raise exceptions.LoginFail
        if not user.active:
            raise exceptions.AccountDisabled
        # Per OWASP: do not transition pre-session to session: might result
        # in session fixation attack.
        session.delete(presession_record)
        session_token = security.create_session_token()
        record = Session(
            csrf_token=security.create_CSRF_token(),
            ip_address=request.client_addr,
            session_token=security.fast_hash(session_token),
            user_agent=request.user_agent,
            user=user)
        session.add(record)
        user.last_login = datetime.now()
    cookie = security.create_session_cookie(session_token)
    response.set_cookie(**cookie)


def logout(request, response):
    """Log out user, delete session and cookie.

    Args:
        request: webob.Request object.
        response: webob.Response object.
    """
    session_token = request.cookies.get('sessionid')
    hashed = security.fast_hash(session_token)
    with session_scope() as session:
        sid = session.query(Session).filter_by(
            session_token=hashed).first()
        logging.info(
            f'{config["APP_NAME"]} logout: {sid.user.email} ip: {request.client_addr}')
        session.delete(sid)
    # Per OWASP: to close a session and invalidate a cookie,
    # provide an empty value for session id.
    response.set_cookie(name='sessionid', value='')


def setup():
    """Configure database, creating tables if needed."""
    engine = create_engine(
        config['DATABASE_URL'],
        echo=False,
        pool_recycle=3600)
    # Create tables
    Base.metadata.create_all(engine)
    SQLSession.configure(bind=engine)


def login_required(func=None, redirect=True):
    """Validate session token in cookie.

    Use as a decorator.

    Args:
        request: webob.Request object
        response:  webob.Response object
        kwargs: dictionary of URL keyword arguments.

    Raises:
        HTTPRedirect: redirect to config.LOGIN_URL if set and redirect == True.
        LoginFail: if config.LOGIN_URL not set or redirect == False.

    Note:
        Decorators with optional arguments are tricky. The template for this
        decorator is taken from The Python Cookbook, section 9.6.
    """
    if func is None:
        return partial(login_required, redirect=redirect)

    @wraps(func)
    def wrapper(*args, **kwargs):
        request = kwargs.get('request', args[0])
        try:
            user = get_session(request).user
            request.user = user
        except exceptions.LoginFail:
            login_url = config['LOGIN_URL']
            if login_url and redirect:
                raise exceptions.HTTPRedirect(login_url)
            else:
                raise exceptions.LoginFail
        # Class-based handler: RESTful API.
        if inspect.isclass(func):
            handler = getattr(func(), request.method.lower(), None)
            if handler:
                handler(*args, **kwargs)
            else:
                raise exceptions.LoginFail
        else:
            return func(*args, **kwargs)
    return wrapper


def update_password(userid, password):
    """Change password for user.

    Args:
        userid: integer.
        password: new password string.
    """
    with session_scope() as session:
        user = session.query(User).filter_by(id=userid).first()
        salt = security.gensalt()
        user.pwhash = security.slow_hash(password, salt)
        user.salt = salt


def validate_CSRF(request):
    """Return CSRF token if valid.

    Args:
        request: webob.Request object.

    Raises:
        CSRFTokenFail: CSRF token not found in session database.
        LoginFail: user agent mismatch, or session expired.
    """
    try:
        # CSRF token in form or Ajax headers.
        token = request.POST.get(
            'CSRFToken',
            request.environ.get('HTTP_X_CSRFTOKEN'))
        with session_scope() as sql_session:
            record = sql_session.query(Session).filter_by(
                csrf_token=token).first()
            # If session cookie age isn't set, the cookie is valid as long
            # as the browser is open.
            age = config['SESSION_COOKIE_AGE']
            if age:
                expire_date = record.date_created + timedelta(seconds=age)
                if datetime.now() > expire_date:
                    raise exceptions.LoginFail
            if record.user_agent != request.user_agent:
                raise exceptions.LoginFail
            if not record:
                raise exceptions.CSRFTokenFail
        return token
    except Exception:
        raise exceptions.CSRFTokenFail


@contextmanager
def session_scope():
    """Context manager for database operations.

    Automatically handles database commit, rollback, and close.
    Taken from SQLAlchemy docs.

    Use as a decorator.
    """
    session = SQLSession()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

