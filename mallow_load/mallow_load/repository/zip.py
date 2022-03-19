from mallow_load.mallow_load.error import NotPresentInRepositoryError
from mallow_load.mallow_load.model import ZipCode
from mallow_load.mallow_load.repository.base import Repository


class ZipCodeRepository(Repository):
    def __init__(self) -> None:
        self._repository: dict[str, ZipCode] = dict()

    @property
    def repository(self):
        return self._repository

    def get(self, key: str) -> ZipCode:
        if not (item := self.repository.get(key)):
            raise NotPresentInRepositoryError(f"{item} not present in repository.")
        return item

    def _add_row_to_repository(self, row: dict[str, str]) -> None:
        z = ZipCode.from_dict(row)
        self.repository[z.zip_code] = z
