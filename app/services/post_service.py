from repositories.post_repo import PostRepository
from repositories.tag_repo import TagRepository
from models.post import Post
from models.tag import Tag
from schemas.post import PostCreate, PostRead

class PostService:
    def __init__(self, post_repo: PostRepository, tag_repo: TagRepository):
        self.post_repo = post_repo
        self.tag_repo = tag_repo

    async def create_post(self, payload: PostCreate, owner_id: int) -> PostRead:
        post = Post(title=payload.title, content=payload.content, owner_id=owner_id)
        tags_objs = []
        for tname in payload.tags or []:
            # handle tags: create if not exists then append
            tag = await self.tag_repo.get_by_name(tname)
            if not tag:
                tag = Tag(name=tname)
                await self.tag_repo.create(tag)
            tags_objs.append(tag)
        post.tags = tags_objs
        p = await self.post_repo.create(post)
        
        response_data = {
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "owner_id": p.owner_id,
            "tags": [{"id": t.id, "name": t.name} for t in tags_objs],
        }
        
        return PostRead.model_validate(response_data)

    async def get_post(self, post_id: int):
        return await self.post_repo.get(post_id)
