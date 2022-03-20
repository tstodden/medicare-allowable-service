from mallow_load.mallow_load.error import NotPresentInRepositoryError
from mallow_load.mallow_load.model import Charge
from mallow_load.mallow_load.repository.base import Repository


class ChargeRepository(Repository):
    def __init__(self) -> None:
        self._repository: dict[tuple[str, str], Charge] = dict()

    @property
    def repository(self) -> dict[tuple[str, str], Charge]:
        return self._repository

    def get(self, key: tuple[str, str]) -> Charge:
        if not (item := self.repository.get(key)):
            raise NotPresentInRepositoryError(f"{item} not present in repository.")
        return item

    def _add_row_to_repository(self, row: dict[str, str]) -> None:
        charge = Charge.from_dict(row)
        self.repository[(charge.charge_code, charge.modifier)] = charge
