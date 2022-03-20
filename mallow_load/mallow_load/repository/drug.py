from mallow_load.mallow_load.error import NotPresentInRepositoryError
from mallow_load.mallow_load.model import Drug
from mallow_load.mallow_load.repository.base import Repository


class DrugRepository(Repository):
    def __init__(self) -> None:
        self._repository: dict[tuple[str, int], Drug] = dict()

    @property
    def repository(self) -> dict[tuple[str, int], Drug]:
        return self._repository

    def get(self, key: tuple[str, int]) -> Drug | None:
        if not (item := self.repository.get(key)):
            return None
        return item

    def _add_row_to_repository(self, row: dict[str, str]) -> None:
        drug = Drug.from_dict(row)
        self.repository[(drug.charge_code, drug.quarter)] = drug
