from mallow_load.mallow_load.controller.database import ElasticsearchController
from mallow_load.mallow_load.controller.storage import GoogleStorageController
from mallow_load.mallow_load.repository import RepositoryType


class ApplicationService:
    def __init__(self) -> None:
        self.elastic = ElasticsearchController()
        self.google = GoogleStorageController()

    def load_index_for_year(self, index: str, year: int) -> None:
        if index == "gpci_by_year":
            self._load_gpci_by_year_index(year)
        else:
            raise ValueError(f"{index} is not a valid index.")

    def _load_gpci_by_year_index(self, year: int) -> None:
        zip_repo = self.google.load_repository(RepositoryType.ZIP_CODE, year)
        mac_locality_repo = self.google.load_repository(
            RepositoryType.MAC_LOCALITY, year
        )
        print(zip_repo.repository)
        print(mac_locality_repo.repository)
