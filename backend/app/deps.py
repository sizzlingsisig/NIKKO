"""Auth dependency for the admin surface (PRD FR-4.1 token gate)."""

import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from . import config

bearer_scheme = HTTPBearer(auto_error=False, description="Admin token from ADMIN_TOKEN")


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid admin token.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def require_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    """Return the caller's token, or raise 401.

    Compares in constant time so a wrong token leaks no timing signal.
    """
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise _unauthorized()
    if not secrets.compare_digest(credentials.credentials, config.ADMIN_TOKEN):
        raise _unauthorized()
    return credentials.credentials
