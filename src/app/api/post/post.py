from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, Query, UploadFile, status
from fastapi.responses import FileResponse
from pydantic import ValidationError

from app.api.post.depends import (
    get_create_post_case,
    get_delete_post_case,
    get_edit_post_case,
    get_get_post_by_id_case,
    get_get_post_image_by_id_case,
    get_get_post_list_case,
)
from app.core.exceptions.auth_exception import ForbiddenException
from app.core.exceptions.file_domain_exceptions import (
    NoImageException,
    UploadFileHasNotNameException,
    UploadFileIsNotImageException,
)
from app.core.exceptions.post_domain_exception import (
    GetPostListException,
    PostNotCreatedException,
    PostNotDeletedException,
    PostNotFoundByIdException,
)
from app.core.exceptions.user_domain_exception import UserNotFoundByUsernameException
from app.domain.post.create_post import CreatePostUseCase
from app.domain.post.delete_post import DeletePostUseCase
from app.domain.post.edit_post import EditPostUseCase
from app.domain.post.get_post import GetPostByIdUseCase
from app.domain.post.get_post_image import GetPostImageByIdUseCase
from app.domain.post.get_post_list import GetPostListUseCase
from app.schemas.post import CreatePostSchema, EditPostSchema, ResponsePostSchema
from app.schemas.user import ResponseUserSchema
from app.services.auth import AuthService

router = APIRouter()


@router.get(
    "/posts", status_code=status.HTTP_200_OK, response_model=list[ResponsePostSchema]
)
async def get_post_list(
    category_slug: str = Query(default=None),
    location_name: str = Query(default=None),
    use_case: GetPostListUseCase = Depends(get_get_post_list_case),
):
    try:
        return await use_case.execute(category_slug, location_name)
    except GetPostListException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )


@router.get(
    "/posts/{id}", status_code=status.HTTP_200_OK, response_model=ResponsePostSchema
)
async def get_post_by_id(
    id: int, use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_case)
) -> ResponsePostSchema:
    try:
        return await use_case.execute(id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@router.get("/posts/{id}/image", status_code=status.HTTP_200_OK)
async def get_post_image_by_id(
    id: int, use_case: GetPostImageByIdUseCase = Depends(get_get_post_image_by_id_case)
) -> FileResponse:
    try:
        return await use_case.execute(id)
    except (PostNotFoundByIdException, NoImageException) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@router.post(
    "/posts",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponsePostSchema,
)
async def create_post(
    title: str = Form(...),
    text: str = Form(...),
    category_slug: str = Form(...),
    publicated_at: datetime | None = Form(None),
    location_name: str | None = Form(None),
    is_published: bool | None = Form(None),
    image: UploadFile | None = None,
    use_case: CreatePostUseCase = Depends(get_create_post_case),
    user: ResponseUserSchema = Depends(AuthService.get_current_user)
) -> ResponsePostSchema:
    try:
        post_data = CreatePostSchema(
            is_published=is_published,
            title=title,
            text=text,
            publicated_at=publicated_at,
            category_slug=category_slug,
            location_name=location_name
        )
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=exc.errors()
        )

    try:
        return await use_case.execute(user.username, post_data, image)
    except PostNotCreatedException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except (UploadFileIsNotImageException, UploadFileHasNotNameException) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=exc.get_detail()
        )


@router.patch(
    "/posts/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponsePostSchema
)
async def edit_post(
    id: int,
    title: str | None = Form(None),
    text: str | None = Form(None),
    category_slug: str | None = Form(None),
    location_name: str | None = Form(None),
    is_published: bool | None = Form(None),
    image: UploadFile | None = None,
    use_case: EditPostUseCase = Depends(get_edit_post_case),
    user: ResponseUserSchema = Depends(AuthService.get_current_user)
) -> ResponsePostSchema:
    try:
        post_data = EditPostSchema(
            title=title,
            text=text,
            category_slug=category_slug,
            location_name=location_name,
            is_published=is_published
        )
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=exc.errors()
        )

    try:
        return await use_case.execute(user.username, id, post_data, image)
    except ForbiddenException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )
    except PostNotCreatedException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except (UploadFileIsNotImageException, UploadFileHasNotNameException) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=exc.get_detail()
        )


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    use_case: DeletePostUseCase = Depends(get_delete_post_case),
    user: ResponseUserSchema = Depends(AuthService.get_current_user)
) -> None:
    try:
        await use_case.execute(
            post_id=id, username=user.username, is_user_admin=user.is_admin
        )
    except PostNotDeletedException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except ForbiddenException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )
