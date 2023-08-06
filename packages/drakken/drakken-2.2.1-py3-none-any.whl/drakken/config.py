import json


def read_dict(d):
    """Read dictionary d and update config."""
    config.update(d)


def read_file(path):
    """Read JSON config file and update config."""
    with open(path, 'r') as f:
        d = json.load(f)
    config.update(d)


# Default values.
config = {
    'APP_NAME': 'Drakken app',  # Used for logging.
    'LOGIN_URL': '',
    'USERNAME': False,
    'SESSION_COOKIE_SECURE': False,
    'DATABASE_URL': 'sqlite:///demo.sqlite3',
    'STATIC_DIR': 'static',
    'TEMPLATE_DIR': 'templates',
    'SESSION_COOKIE_AGE': 86400,  # Sessions last 1 day.
    'CSRF_TOKEN_BYTES': 16,
    'SALT_BYTES': 16,
    'SESSION_TOKEN_BYTES': 16,
    # Per OWASP: min password length: 8, max password length: 64 to
    # prevent password DOS attacks.
    'MIN_PASSWORD_LENGTH': 8,
    'MAX_PASSWORD_LENGTH': 64,
}

