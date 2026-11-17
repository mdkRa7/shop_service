from application.dtos import DecorationDTO
from application.interfaces import ActiveRepositoryProtocol


class GetDecorations:
    def __init__(self, repo: ActiveRepositoryProtocol):
        self._repo = repo

    async def execute(self) -> list[DecorationDTO]:
        decorations = await self._repo.get_all_active()
        decorations.sort(key=lambda d: (d.price, d.name))
        return [DecorationDTO(id=d.id, name=d.name, price=d.price) for d in decorations]
