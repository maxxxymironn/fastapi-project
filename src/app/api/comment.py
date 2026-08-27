from fastapi import APIRouter, status

from app.schemas.comment import CreateCommentSchema, ResponseCommentSchema


router = APIRouter()


@router.get(
    "/posts/{post_id}/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCommentSchema
)
async def get_comments(post_id: int):
    pass


@router.post(
    "/posts/{post_id}/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCommentSchema
)
async def create_comment(post_id: int, CreateCommentSchema):
    pass


@router.patch(
    "/posts/{post_id}/comments",
    status_code=status.HTTP_206_PARTIAL_CONTENT,
    response_model=ResponseCommentSchema
)
async def edit_comment(post_id: int, comment_id: int, new_text: str | None, image_url: str | None):
    pass


@router.delete(
    "/posts/{post_id}/comments",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(post_id: int, comment_id: int):
    pass