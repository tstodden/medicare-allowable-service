from mallow_load.mallow_load.error import NotPresentInRepositoryError
from mallow_load.mallow_load.model import Lab
from mallow_load.mallow_load.repository.base import Repository


class LabRepository(Repository):
    def __init__(self) -> None:
        self._repository: dict[tuple[str, str], Lab] = dict()

    @property
    def repository(self) -> dict[tuple[str, str], Lab]:
        return self._repository

    def get(self, key: tuple[str, str]) -> Lab | None:
        if not (item := self.repository.get(key)):
            return None
        return item

    def _add_row_to_repository(self, row: dict[str, str]) -> None:
        lab = Lab.from_dict(row)
        self.repository[(lab.charge_code, lab.modifier)] = lab
