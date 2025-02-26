from passlib.context import CryptContext
from fastapi import Depends, Security, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from models.jwtToken_model import Token, TokenData
from models.user_model import User

passlib_context = CryptContext(schemes=["bcrypt"])


JWT_KEY = "8064eba13ae82a8e4ff46d015818561c34bd956ca0f079596e06ea93d2f94d6c"
ALGO_JWT = "HS256"
JWT_TOKEN_EXPIRY_TIME = 30  # in mins


jwt_scheme = OAuth2PasswordBearer(tokenUrl="token", scheme_name="")


def create_pass_hash(password: str):

    hashed_pass = passlib_context.hash(password)

    return hashed_pass


def verify_pass(plain_pass: str, hashed_pass: str):

    return passlib_context.verify(plain_pass, hashed_pass)


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(JWT_TOKEN_EXPIRY_TIME)
    data_to_encode.update({"exp": expire})

    jwt_encoded = jwt.encode(data_to_encode, JWT_KEY, algorithm=ALGO_JWT)

    return jwt_encoded


async def get_curr_user(token: Annotated[str, Depends(jwt_scheme)]) -> User:
    from services.user_service import get_user_by_id

    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials",
                                         headers={"WWW-Authenticate": "Bearer"},)

    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=ALGO_JWT)
        userID = payload.get("user_id")
        if userID is None:
            raise credential_exception
        token_data = TokenData(user_id=userID)
    except InvalidTokenError:
        raise credential_exception
    user = get_user_by_id(user_id=token_data.user_id)
    if user is None:
        raise credential_exception
    return user

# async def
