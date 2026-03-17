"""Password generation utilities."""

from __future__ import annotations

import secrets
import string

_ALLOWED_CHARS = (
    string.ascii_lowercase
    + string.ascii_uppercase
    + string.digits
    + "!@#$%^&*"
)
_EXCLUDED_CHARS = set("iIl1o0O")
_PASSWORD_CHARS = "".join(char for char in _ALLOWED_CHARS if char not in _EXCLUDED_CHARS)


def generate_password(length: int = 13) -> str:
    """Generate a readable password with ambiguous characters removed."""

    if length <= 0:
        raise ValueError("length must be greater than 0")
    return "".join(secrets.choice(_PASSWORD_CHARS) for _ in range(length))


__all__ = ["generate_password"]
