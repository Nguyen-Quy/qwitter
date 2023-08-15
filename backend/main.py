from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import qweets, user

import uvicorn

app = FastAPI(
    title="Qweeter",
    docs_url="/docs",
    description="Qweeter api",
)

origins = [
    "http://localhost:8081",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(qweets.router)
app.include_router(user.router)
# app.include_router(qweet_users.router)
# app.include_router(auth_user.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
