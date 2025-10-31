from models.tag import Tag
from repositories.tag_repo import TagRepository
from schemas.tag import TagRead


class TagService:
    def __init__(self, repo: TagRepository):
        self.repo = repo

    async def create_tag(self, name: str) -> TagRead:
        existing = await self.repo.get_by_name(name)
        if existing:
            raise ValueError("Tag already exists")
        tag = Tag(name=name)
        t = await self.repo.create(tag)
        return TagRead.model_validate(t)

    async def list_tags(self, limit: int = 50, offset: int = 0) -> list[TagRead]:
        tags = await self.repo.list(limit=limit, offset=offset)
        return [TagRead.model_validate(t) for t in tags]

