from starlette.status import HTTP_405_METHOD_NOT_ALLOWED
from datetime import datetime

from fastapi import APIRouter, status, HTTPException

from app.schemas.post import PostResponseSchema, PostCreateSchema


router = APIRouter()


@router.get(
    "/posts", 
    status_code=status.HTTP_200_OK
)
async def get_posts():
    return {"hello": "world!"}
    

@router.get(
    "/posts/{post_id}", 
    status_code=status.HTTP_200_OK, 
    response_model=PostResponseSchema
)
async def get_post_detail(post_id: int):
    default_post = PostResponseSchema(
        id=1, title="title", text="text-text-text",
        is_published=True, author_id=1, 
        publicated_at=datetime.now(),
        updated_at=datetime.now()
    )
    return default_post


@router.post(
    "/posts", 
    status_code=status.HTTP_201_CREATED, 
    response_model=PostResponseSchema
)
async def create_post(post: PostCreateSchema):
    if len(post.title) == 0:
        raise HTTPException(
            detail="post must have title",
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )

    new_post = {
        "id": 1,
        "title": post.title,
        "text": post.text,
        "is_pub": post.is_published,
        "image": post.image_path,
        "author_id": post.author_id,
        "category_id": post.category_id,
        "location_id": post.location_id,
        "pub_at": post.publicated_at,
        "updated_at": post.publicated_at
    }
    
    return PostResponseSchema.model_validate(obj=new_post)


@router.patch(
    "/posts/{post_id}", 
    status_code=status.HTTP_200_OK, 
    response_model=PostResponseSchema
)
async def edit_post(post_id: int, post: PostCreateSchema):
    default_post = PostResponseSchema(
        id=5, title="title", text="text-text-text",
        is_published=True, author_id=1, 
        publicated_at=datetime.now(),
        updated_at=datetime.now()
    )

    if post_id == 5:
        return {"status": "ok"}

    return HTTPException(
        detail="no babe",
        status_code=status.HTTP_400_BAD_REQUEST
    )


@router.delete(
    "/posts/{post_id}", 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post(post_id: int):
    return {"status": "deleted"}

