from fastapi import HTTPException, APIRouter, status, Depends

from app.domain.comment.get_comment_list import GetCommentListUseCase
from app.domain.comment.create_comment import CreateCommentUseCase
from app.domain.comment.edit_comment import EditCommentUseCase
from app.domain.comment.delete_comment import DeleteCommentUseCase
from app.schemas.comment import (
    CreateCommentSchema, 
    ResponseCommentSchema, 
    EditCommentSchema
)
from app.api.depends import (
    get_case_get_comment_list,
    get_case_create_comment,
    get_case_edit_comment,
    get_case_delete_comment
)


router = APIRouter()


@router.get(
    "/posts/{post_id}/comments",
    status_code=status.HTTP_200_OK,
    response_model=list[ResponseCommentSchema]
)
async def get_comment_list(
    post_id: int,
    use_case: GetCommentListUseCase = Depends(get_case_get_comment_list)
) -> list[ResponseCommentSchema]:
    try:
        return use_case.execute(post_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post(
    "/posts/{post_id}/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCommentSchema
)
async def create_comment(
    post_id: int, 
    comment_data: CreateCommentSchema,
    use_case: CreateCommentUseCase = Depends(get_case_create_comment)
) -> ResponseCommentSchema:
    try:
        return use_case.execute(post_id, comment_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.patch(
    "/posts/{post_id}/comments",
    status_code=status.HTTP_206_PARTIAL_CONTENT,
    response_model=ResponseCommentSchema
)
async def edit_comment(
    post_id: int,
    user_id: int,
    comment_id: int,
    comment_data: EditCommentSchema,
    use_case: EditCommentUseCase = Depends(get_case_edit_comment)
) -> ResponseCommentSchema:
    try:
        return use_case.execute(post_id, user_id, comment_id, comment_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete(
    "/posts/{post_id}/comments",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(
    post_id: int,
    user_id: int,
    comment_id: int,
    use_case: DeleteCommentUseCase = Depends(get_case_delete_comment)
) -> None:
    try:
        use_case.execute(post_id, user_id, comment_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)