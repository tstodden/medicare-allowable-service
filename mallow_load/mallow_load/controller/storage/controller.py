import os
from tempfile import SpooledTemporaryFile

from google.cloud import storage
from google.cloud.storage.blob import Blob

from mallow_load.mallow_load.controller.storage.constant import BucketPrefix
from mallow_load.mallow_load.repository import (
    MacLocalityRepository,
    Repository,
    RepositoryType,
    ZipCodeRepository,
)


class GoogleStorageController:
    _cache: dict[RepositoryType, Repository] = dict()

    def __init__(self) -> None:
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(os.environ["MALLOW_BUCKET"])

    def load_repository(self, type_: RepositoryType, year: int) -> Repository:
        result = None
        if type_ == RepositoryType.ZIP_CODE:
            result = self._load_zip_code_repository(year)
        elif type_ == RepositoryType.MAC_LOCALITY:
            result = self._load_mac_locality_repository(year)
        else:
            raise ValueError(f"{type_} is not a valid repository type.")
        return result

    def _load_zip_code_repository(self, year: int) -> Repository:
        blob = self.bucket.get_blob(f"{BucketPrefix.ZIP_DATA.value}/zip-{year}.csv")
        return self._add_blob_to_repository(blob, ZipCodeRepository())

    def _load_mac_locality_repository(self, year: int) -> Repository:
        blob = self.bucket.get_blob(f"{BucketPrefix.GPCI_DATA.value}/gpci-{year}.csv")
        return self._add_blob_to_repository(blob, MacLocalityRepository())

    def _add_blob_to_repository(self, blob: Blob, repository: Repository) -> Repository:
        with SpooledTemporaryFile(mode="w") as tmp_file:
            tmp_file.write(blob.download_as_text())
            tmp_file.seek(0)
            repository.add_csv_file(tmp_file)
        return repository
