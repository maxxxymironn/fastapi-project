from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.user import router as user_router
from app.api.post import router as post_router
from app.api.comment import router as comment_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(user_router, prefix="/api/v1", tags=["Profile APIs"])
    app.include_router(post_router, prefix="/api/v1", tags=["Post APIs"])
    app.include_router(comment_router, prefix="/api/v1", tags=["Comment APIs"])

    return app