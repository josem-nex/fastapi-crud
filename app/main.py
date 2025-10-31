from fastapi import FastAPI
from api.routers import users, posts, tags, comments
from middleware.timing import TimingMiddleware
from db.base import Base
from db.session import engine

app = FastAPI(title="FastAPI CRUD")
app.add_middleware(TimingMiddleware)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
