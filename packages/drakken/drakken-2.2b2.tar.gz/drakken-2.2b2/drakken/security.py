"""Session security module."""
import hashlib
import secrets

from .config import config


def create_CSRF_token():
    """Create CSRF token.

    Returns:
        String CSRF token.
    """
    return secrets.token_urlsafe(config['CSRF_TOKEN_BYTES'])


def create_session_cookie(token):
    """Create session cookie from token string.

    To close session when browser closes, set SESSION_COOKIE_AGE = 0.

    Args:
        token: unique session ID string.

    Returns:
        Dictionary: For WebOb.Response.set_cookie().
    """
    cookie = dict(name='sessionid', value=token,
                  secure=config['SESSION_COOKIE_SECURE'],
                  httponly=True, samesite='strict',
                  overwrite=True)
    age = config['SESSION_COOKIE_AGE']
    if age:
        cookie['max_age'] = age
    return cookie


def create_session_token():
    """Create session token aka session ID.

    Returns:
        Session token string.
    """
    return secrets.token_urlsafe(
        config['SESSION_TOKEN_BYTES'])


def gensalt():
    """Create salt.

    Returns:
        Password salt string.
    """
    return secrets.token_urlsafe(config['SALT_BYTES'])


def fast_hash(s):
    """Hash string s using SHA256.

    Use on session IDs etc where speed is essential.

    Args:
        s: string to be hashed.

    Returns:
        Hashed input string.
    """
    return hashlib.sha256(s.encode()).hexdigest()


def slow_hash(s, salt):
    """Hash string s with salt.

    Use on passwords and password reset tokens before storing in the
    database. It's slow so don't use on session IDs.

    Uses scrypt: designed to read and write randomly to a lot of memory, This
    kills the advantage ASICs have in cracking passwords and makes
    parallelization prohibitive. n,r,p values suggested by OWASP.

    Args:
        s: string to be salted.
        salt: random string added to input string.

    Returns:
        Input string hashed into bytes.
    """
    return hashlib.scrypt(password=s.encode(),
                          salt=salt.encode(), n=16384, r=8, p=1)


def verify(s, salt, h):
    """Return True if string slow-hashed with salt matches hash.

    Args:
        s: string to be tested.
        salt: random string added to input string.
        h: hash bytes.

    Returns:
        True if string + salt matches hash.
    """
    return slow_hash(s, salt) == h

