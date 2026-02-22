import time
import jwt
from jwt import InvalidTokenError, ExpiredSignatureError


def issue_access_token(*, sub: str, role: str,
                       secret: str, algorithm: str,
                       issuer: str, audience: str,
                       exp_seconds: int) -> str:
    now = int(time.time())
    payload = {
        "sub": sub,
        "role": role,
        "iat": now,
        "exp": now + exp_seconds,
        "iss": issuer,
        "aud": audience,
    }
    return jwt.encode(payload, secret, algorithm=algorithm)

def verify_access_token(
                        token: str,
                        *,
                        secret: str,
                        algorithm: str,
                        issuer: str,
                        audience: str,
                        ) -> dict:
    """
    verifies signature + exp + iss + aud.
    returns decoded claims dict if valid.
    raises jwt exceptions if invalid.
    """
    return jwt.decode(
        token,
        secret,
        algorithms=[algorithm],
        issuer=issuer,
        audience=audience,
        options={
            "require": ["exp", "iat", "iss", "sub"],        # ensure core claims exist
        }
    )

