from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from app.api.comment.depends import (
    get_create_comment_case,
    get_delete_comment_case,
    get_edit_comment_case,
    get_get_comment_image_by_id_case,
    get_get_comment_list_case,
)
from app.core.exceptions.auth_exception import ForbiddenException
from app.core.exceptions.comment_domain_exception import (
    CommentNotCreatedException,
    CommentNotDeletedException,
    CommentNotFoundException,
    GetCommentListException,
)
from app.core.exceptions.file_domain_exceptions import NoImageException
from app.core.exceptions.post_domain_exception import PostNotFoundByIdException
from app.domain.comment.create_comment import CreateCommentUseCase
from app.domain.comment.delete_comment import DeleteCommentUseCase
from app.domain.comment.edit_comment import EditCommentUseCase
from app.domain.comment.get_comment_image import GetCommentImageByIdUseCase
from app.domain.comment.get_comment_list import GetCommentListUseCase
from app.schemas.comment import ResponseCommentSchema
from app.schemas.user import ResponseUserSchema
from app.services.auth import AuthService

router = APIRouter()


@router.get(
    "/posts/{post_id}/comments",
    status_code=status.HTTP_200_OK,
    response_model=list[ResponseCommentSchema],
)
async def get_comment_list(
    post_id: int, use_case: GetCommentListUseCase = Depends(get_get_comment_list_case)
) -> list[ResponseCommentSchema]:

    try:
        return await use_case.execute(post_id)
    except GetCommentListException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )


@router.get(
    "/posts/{post_id}/comments/{comment_id}/image",
    status_code=status.HTTP_200_OK
)
async def get_comment_image(
    post_id: int, comment_id: int,
    use_case: GetCommentImageByIdUseCase = Depends(get_get_comment_image_by_id_case)
) -> FileResponse:
    try:
        return await use_case.execute(post_id, comment_id)
    except (
        PostNotFoundByIdException,
        CommentNotFoundException,
        NoImageException
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@router.post(
    "/posts/{post_id}/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCommentSchema,
)
async def create_comment(
    post_id: int,
    text: str = Form(...),
    image: UploadFile | None = None,
    use_case: CreateCommentUseCase = Depends(get_create_comment_case),
    user: ResponseUserSchema = Depends(AuthService.get_current_user)
) -> ResponseCommentSchema:
    try:
        return await use_case.execute(post_id, user.id, text, image)
    except CommentNotCreatedException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )


@router.patch(
    "/posts/{post_id}/comments",
    status_code=status.HTTP_206_PARTIAL_CONTENT,
    response_model=ResponseCommentSchema,
)
async def edit_comment(
    post_id: int,
    comment_id: int = Form(...),
    text: str | None = Form(...),
    image: UploadFile | None = None,
    use_case: EditCommentUseCase = Depends(get_edit_comment_case),
    user: ResponseUserSchema = Depends(AuthService.get_current_user)
) -> ResponseCommentSchema:
    try:
        return await use_case.execute(post_id, user.id, comment_id, text, image)
    except ForbiddenException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )
    except CommentNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@router.delete("/posts/{post_id}/comments", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    post_id: int,
    comment_id: int,
    use_case: DeleteCommentUseCase = Depends(get_delete_comment_case),
    user: ResponseUserSchema = Depends(AuthService.get_current_user)
) -> None:
    try:
        await use_case.execute(post_id, comment_id, user.id, user.is_admin)
    except ForbiddenException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )
    except CommentNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except CommentNotDeletedException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )
