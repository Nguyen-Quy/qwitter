from typing import Union, Any
from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .utils import (
    JWT_SECRET_KEY,
    JWT_REFRESH_SECRET_KEY,
    ALGORITHM,
    create_access_token,
    create_refresh_token,
)
from jose import jwt, JWTError
from pydantic import ValidationError
from models import qweet_user, UserBase


oauth_bearer = OAuth2PasswordBearer(tokenUrl="/users/login", scheme_name="JWT")


def decode_token(secret_key, token: str = Depends(oauth_bearer)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])

        if datetime.fromtimestamp(payload["exp"]) <= datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload

    except (JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


def get_current_user(token: str = Depends(oauth_bearer)):
    payload = decode_token(JWT_SECRET_KEY, token)

    user: Union[dict[str, Any], None] = qweet_user.find_one(
        {"username": payload["sub"]}
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return UserBase(**user)


def get_refresh_token(token: str = Depends(oauth_bearer)):
    payload = decode_token(JWT_REFRESH_SECRET_KEY, token)
    username = payload["sub"]

    return {
        "access_token": create_access_token(username),
        "refresh_token": create_refresh_token(username),
    }
