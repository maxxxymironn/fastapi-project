from app.schemas.post import CreatePostSchema, ResponsePostSchema
from app.infrastucture.database import db
from app.infrastucture.repositories.post import PostRepository


class CreatePostUseCase:
    def __init__(self): 
        self._db = db
        self._repo = PostRepository()

    async def execute(self, post_data: CreatePostSchema) -> ResponsePostSchema:
        with self._db.session() as session:
            post = await self._repo.create_post(session, post_data)
        
        return ResponsePostSchema.model_validate(post)
        