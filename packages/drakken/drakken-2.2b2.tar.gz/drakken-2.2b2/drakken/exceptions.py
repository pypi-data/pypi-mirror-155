"""Drakken exception classes and functions go here."""

class AccountDisabled(Exception):
    """Account disabled: user.active = False."""
    pass

class AuthenticateFail(Exception):
    """Email/password failure."""
    pass


class BadRequest(Exception):
    """400 Bad request."""
    pass


class CSRFTokenFail(Exception):
    """CSRF token failure."""
    pass


class EmailAddressTaken(Exception):
    """Email address already taken."""
    pass


class Forbidden(Exception):
    """403 Forbidden request.

    Yes, we understood your request, and no, we're not going to do it.
    """
    pass


class LoginFail(Exception):
    """Bad session ID."""
    pass


class NotFound(Exception):
    """404 File not found.

    To supply a 404 page, put a file named 404.html in the top-level
    templates folder.
    """
    pass


class PasswordLength(Exception):
    """Password too long or too short."""
    pass


class UserNameTaken(Exception):
    """User name already taken."""
    pass


def redirect(path, status_code=302):
    """Friendly wrapper to raise HTTPRedirect exception.

    Allows you to `redirect()` instead of `raise HTTPRedirect()`.

    Args:
        path: string path redirected to.
        status_code: response status code integer. Default is 302.
    """
    raise HTTPRedirect(path, status_code)


class HTTPRedirect(Exception):
    """HTTP Redirect (302)."""

    def __init__(self, path, status_code=302):
        """Initialize.

        Args:
            path: string path redirected to.
            status_code: response status code integer. Default is 302.
        """
        self.path = path
        self.status_code = status_code
        super().__init__()

