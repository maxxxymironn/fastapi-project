import shutil
from uuid import uuid4

from fastapi import UploadFile

from app.core.exceptions.file_domain_exceptions import (
    UploadFileHasNotNameException,
    UploadFileIsNotImageException,
)


def get_image_name(post_image: UploadFile | None) -> str | None:
    if not post_image:
        return None

    filename: str | None = post_image.filename
    if not filename:
        raise UploadFileHasNotNameException()
    image_format = filename.split(".")[-1]
    if ("jpeg", "jpg").count(image_format) == 0:
        raise UploadFileIsNotImageException()

    image_name: str = str(uuid4())
    image_path: str = f"./images/{image_name}.jpeg"

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(post_image.file, buffer)

    return image_name
