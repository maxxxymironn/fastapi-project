from app.core.exceptions.database_exception import EntityListException
from app.core.exceptions.post_domain_exception import GetPostListException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.post import PostRepository
from app.schemas.post import ResponsePostSchema


class GetPostListUseCase:
    def __init__(self):
        self._db = db
        self._repo = PostRepository()

    async def execute(
        self, category_slug: str | None, location_name: str | None
    ) -> list[ResponsePostSchema]:
        try:
            async with self._db.session() as session:
                if not category_slug and not location_name:
                    post_list = await self._repo.get_post_list(session)
                elif not category_slug:
                    post_list = await self._repo.get_post_list_by_location(
                        session, location_name.lower()  # pyrefly: ignore [bad-argument-type, missing-attribute]
                    )
                elif not location_name:
                    post_list = await self._repo.get_post_list_by_category(
                        session, category_slug.lower()
                    )
                else:
                    post_list = await self._repo.get_post_list_by_category_and_location(
                        session, category_slug.lower(), location_name.lower()
                    )
        except EntityListException:
            raise GetPostListException()

        return [ResponsePostSchema.model_validate(post) for post in post_list]
