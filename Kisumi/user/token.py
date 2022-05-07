from .client.components.constants.tokens import AuthType
from state import config
from typing import TypedDict, Optional
from jwt import JWT
from jwt.exceptions import JWTDecodeError
import time

jwt_enc = JWT()

class AuthJWT(TypedDict):
    """Type annotations for the authentication JWT."""

    user_id: int
    start: int
    expiry: int
    type: AuthType

# JWT Functionality.
def encode_jwt_dict(jwt_d: AuthJWT) -> str:
    """Encodes a JWT auth dict into a JWT string."""

    # No enums :sob:
    jwt_d_copy = jwt_d.copy()
    jwt_d_copy['type'] = jwt_d_copy['type'].value

    return jwt_enc.encode(
        jwt_d_copy,
        key= config.CRYPT_JWT_SECRET,
    )

def decode_jwt_str(jwt_str: str) -> Optional[AuthJWT]:
    """Decodes a JWT auth str into a dict. Returns `None` on fail."""

    try:
        jwt_dec = jwt_enc.decode(
            jwt_str,
            key= config.CRYPT_JWT_SECRET,
        )
    except JWTDecodeError:
        return None
    
    jwt_dec["type"] = AuthType(jwt_dec["type"])
    return jwt_dec

def confirm_token_expiry(jwt_d: AuthJWT) -> bool:
    """Checks if the token is active time wise."""

    t = time.time()

    return jwt_d['start'] < t < jwt_d['expiry']
