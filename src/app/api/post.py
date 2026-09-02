from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.depends import (
    get_case_create_post,
    get_case_delete_post,
    get_case_edit_post,
    get_case_get_post_by_title,
    get_case_get_post_list,
)
from app.domain.post.use_cases.create_post import CreatePostUseCase
from app.domain.post.use_cases.delete_post import DeletePostUseCase
from app.domain.post.use_cases.edit_post import EditPostUseCase
from app.domain.post.use_cases.get_post_by_title import GetPostByTitleUseCase
from app.domain.post.use_cases.get_post_list import GetPostListUseCase
from app.schemas.post import CreatePostSchema, EditPostSchema, ResponsePostSchema

router = APIRouter()


@router.get(
    "/posts", status_code=status.HTTP_200_OK, response_model=list[ResponsePostSchema]
)
async def get_post_list(
    category_slug: str = Query(default=None),
    use_case: GetPostListUseCase = Depends(get_case_get_post_list),
):
    try:
        # return await use_case.execute(category)
        return await use_case.execute(category_slug)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    "/posts/{id}", status_code=status.HTTP_200_OK, response_model=ResponsePostSchema
)
async def get_post_by_id(
    id: int, use_case: GetPostByTitleUseCase = Depends(get_case_get_post_by_title)
) -> ResponsePostSchema:
    try:
        return await use_case.execute(id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=ResponsePostSchema
)
async def create_post(
    post_data: CreatePostSchema,
    use_case: CreatePostUseCase = Depends(get_case_create_post),
) -> ResponsePostSchema:
    try:
        return await use_case.execute(post_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.patch(
    "/posts/{id}", status_code=status.HTTP_200_OK, response_model=ResponsePostSchema
)
async def edit_post(
    id: int,
    post_data: EditPostSchema,
    use_case: EditPostUseCase = Depends(get_case_edit_post),
) -> ResponsePostSchema:
    try:
        return await use_case.execute(id, post_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int, use_case: DeletePostUseCase = Depends(get_case_delete_post)
) -> None:
    try:
        await use_case.execute(id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
