from application.dtos import FillingDTO
from application.interfaces import ActiveRepositoryProtocol


class GetFillings:
    def __init__(self, repo: ActiveRepositoryProtocol):
        self._repo = repo

    async def execute(self) -> list[FillingDTO]:
        fillings = await self._repo.get_all_active()
        fillings.sort(key=lambda f: (f.price_per_kg, f.name))
        return [
            FillingDTO(id=f.id, name=f.name, price_per_kg=f.price_per_kg)
            for f in fillings
        ]
