from app.infrastucture.database import db
from app.infrastucture.repositories.post import PostRepository
from app.schemas.post import ResponsePostSchema


class GetPostListUseCase:
    def __init__(self):
        self._db = db
        self._repo = PostRepository()

    # async def execute(self, category: str | None):
    # if not category:
    #   call default get_post_list
    # else:
    #   call get_post_list_by_category
    async def execute(self):
        with self._db.session() as session:
            post_list = await self._repo.get_post_list(session)
        
        return [ResponsePostSchema.model_validate(post) for post in post_list]
        
