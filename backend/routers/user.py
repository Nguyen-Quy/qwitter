from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models import UserCreate, TokenRefresh, qweet_user
from .utils import Hasher, create_access_token, create_refresh_token
from .deps import get_current_user, get_refresh_token
import pymongo

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/signup")
async def create_user(data: UserCreate):
    user = qweet_user.find_one({"username": data.username})
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )
    user_dict = data.dict()
    user_dict["password"] = Hasher.get_password_hash(user_dict["password"])
    qweet_user.insert_one(user_dict)
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "Success",
    }


@router.patch("/update")
async def update_user(data: dict, user: UserCreate = Depends(get_current_user)):
    # * user changes password
    curr_user = qweet_user.find_one({"username": user.username})
    result = curr_user
    if "current_pass" in data and "new_pass" in data:
        if check_pass := Hasher.verify_password(
            data["current_pass"], result["password"]
        ):
            result = qweet_user.find_one_and_update(
                {"username": user.username},
                {"$set": {"password": Hasher.get_password_hash(data["new_pass"])}},
                upsert=False,
                return_document=pymongo.ReturnDocument.AFTER,
            )
    # * user changes email & name
    else:
        update_fields = ["email", "fullname"]
        if update_data := {
            field: data[field] for field in update_fields if field in data
        }:
            result = qweet_user.find_one_and_update(
                {"username": user.username},
                {"$set": update_data},
                upsert=False,
                return_document=pymongo.ReturnDocument.AFTER,
            )
    try:
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e

    return {
        "code": 200,
        "message": f"User {user.username} updated successfully",
    }


@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = qweet_user.find_one({"username": form_data.username})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect username",
        )

    hashed_pass = user["password"]
    if check_pass := Hasher.verify_password(form_data.password, hashed_pass):
        return {
            "access_token": create_access_token(user["username"]),
            "refresh_token": create_refresh_token(user["username"]),
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )


@router.get("/me")
def get_me(user: UserCreate = Depends(get_current_user)):
    return user


@router.post("/refresh", response_model=TokenRefresh)
def refresh_token(token: TokenRefresh = Depends(get_refresh_token)):
    return token
