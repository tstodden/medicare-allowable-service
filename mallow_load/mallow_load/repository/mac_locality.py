from mallow_load.mallow_load.error import NotPresentInRepositoryError
from mallow_load.mallow_load.model import MacLocality
from mallow_load.mallow_load.repository.base import Repository


class MacLocalityRepository(Repository):
    def __init__(self) -> None:
        self.repository: dict[tuple[int, int], MacLocality] = dict()

    def get(self, key: tuple[int, int]) -> MacLocality:
        if not (item := self.repository.get(key)):
            raise NotPresentInRepositoryError(f"{item} not present in repository.")
        return item

    def _add_row_to_repository(self, row: dict[str, str]) -> None:
        ml = MacLocality.from_dict(row)
        self.repository[(ml.mac_id, ml.locality_id)] = ml
