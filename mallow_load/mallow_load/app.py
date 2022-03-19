from typing import Any, Iterable

from mallow_load.mallow_load.controller.database import ElasticsearchController
from mallow_load.mallow_load.controller.storage import GoogleStorageController
from mallow_load.mallow_load.repository import (
    RepositoryType,
    ZipCodeRepository,
    MacLocalityRepository,
)


class ApplicationService:
    def __init__(self) -> None:
        self.elastic = ElasticsearchController()
        self.google = GoogleStorageController()

    def load_index_for_year(self, index: str, year: int) -> None:
        if index == "gpci_by_zip":
            self._load_gpci_by_year_index(index, year)
        else:
            raise ValueError(f"{index} is not a valid index.")

    def _load_gpci_by_year_index(self, index: str, year: int) -> None:
        zip_repo = self.google.load_zip_code_repository(year)
        mac_locality_repo = self.google.load_mac_locality_repository(year)
        self.elastic.bulk_load_into_index(
            index, self._gen_gpci_documents(index, zip_repo, mac_locality_repo)
        )

    def _gen_gpci_documents(
        self,
        index: str,
        zip_repo: ZipCodeRepository,
        mac_locality_repo: MacLocalityRepository,
    ) -> Iterable[dict]:
        for zip_ in zip_repo.repository.values():
            ml = mac_locality_repo.get((zip_.mac_id, zip_.locality_id))
            yield {
                "_index": index,
                "zip_code": zip_.zip_code,
                "year": zip_.year,
                "mac_id": zip_.mac_id,
                "locality_id": zip_.locality_id,
                "pw_gpci": ml.pw_gpci,
                "pe_gpci": ml.pe_gpci,
                "mp_gpci": ml.mp_gpci,
            }
