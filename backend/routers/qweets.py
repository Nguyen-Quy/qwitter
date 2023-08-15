from fastapi import APIRouter, Header, HTTPException, status, Depends
from bson import ObjectId
from models import Qweet, qweet, UserCreate
from datetime import datetime
from .user import get_me
from .deps import get_current_user
from pymongo import ReturnDocument

router = APIRouter(
    prefix="/qweet",
    tags=["qweet"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_qweets(user: UserCreate = Depends(get_current_user)):
    qweets = []
    for q in qweet.find({"created_by": user.username}):
        qweet_dict = {"qweet_id": str(q.get("_id")), **q}
        qweet_dict.pop("_id")
        qweets.append(qweet_dict)

    if qweets:
        return {
            "data": qweets,
            "code": 200,
            "message": "Successfully get Qweets",
        }
    else:
        return {"data": qweets, "message": "No data"}


@router.post("/")
async def add_qweet(q: Qweet, user: UserCreate = Depends(get_current_user)):
    qweet_dict = q.dict()
    qweet_dict["created_by"] = str(user.username)
    qweet_dict["created_at"] = datetime.now()
    result = qweet.insert_one(qweet_dict)
    qweet_dict["qweet_id"] = str(result.inserted_id)
    qweet_dict.pop("_id")

    return {
        "data": qweet_dict,
        "code": 200,
        "message": "Qweet added successfully",
    }


@router.get("/{qweet_id}")
async def get_qweet(qweet_id: str):
    if q := qweet.find_one({"_id": ObjectId(qweet_id)}):
        return {
            "data": {"todo_id": str(q.pop("_id")), **q},
            "code": 200,
            "message": "Successfully get Qweet",
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Qweet not found",
    )


@router.patch("/{qweet_id}")
async def update_qweet(qweet_id: str, q: Qweet):
    qweet_dict = q.dict(exclude_unset=True)
    qweet_dict["updated_at"] = datetime.now()
    result = qweet.update_one({"_id": ObjectId(qweet_id)}, {"$set": qweet_dict})
    qweet_dict["qweet_id"] = qweet_id

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Qweet not found",
        )

    return {
        "data": qweet_dict,
        "code": 200,
        "message": f"Qweet data with ID: {qweet_id} successfully updated",
    }


@router.patch("/comment/{qweet_id}")
async def comment_qweet(qweet_id: str, commentData: dict):
    qw = qweet.find_one({"_id": ObjectId(qweet_id)})

    comments = qw["comments"] or []
    new_comment = {"comment": commentData.get("comment")}
    comments.append(new_comment)

    result = qweet.find_one_and_update(
        {"_id": ObjectId(qweet_id)},
        {
            "$set": {
                "commentCount": len(comments),
                "comments": comments,
            }
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    try:
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Qweet not found",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e

    return {
        "code": 200,
        "comment": new_comment,
        "message": "Comment posted successfully",
    }


@router.delete("/{qweet_id}")
async def delete_qweet(qweet_id: str):
    result = qweet.delete_one({"_id": ObjectId(qweet_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Qweet not found",
        )
    return {
        "message": f"Qweet data with ID: {qweet_id} deleted",
        "code": 200,
    }
