import time
import jwt


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