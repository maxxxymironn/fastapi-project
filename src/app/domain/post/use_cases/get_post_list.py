from app.infrastucture.database import db
from app.infrastucture.repositories.post import PostRepository
from app.schemas.post import ResponsePostSchema


class GetPostListUseCase:
    def __init__(self):
        self._db = db
        self._repo = PostRepository()

    async def execute(self, category_slug: str):
        with self._db.session() as session:
            if not category_slug:
                post_list = await self._repo.get_post_list(session)
            else:
                post_list = await self._repo.get_post_list_by_category(session, category_slug)
        
        return [ResponsePostSchema.model_validate(post) for post in post_list]
        
