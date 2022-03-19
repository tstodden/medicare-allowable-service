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

    def load_zip_code_repository(self, year: int) -> ZipCodeRepository:
        blob = self.bucket.get_blob(f"{BucketPrefix.ZIP_DATA.value}/zip-{year}.csv")
        repository = self._add_blob_to_repository(blob, ZipCodeRepository())
        if not isinstance(repository, ZipCodeRepository):
            raise ValueError("Incorrect repository type.")
        return repository

    def load_mac_locality_repository(self, year: int) -> MacLocalityRepository:
        blob = self.bucket.get_blob(f"{BucketPrefix.GPCI_DATA.value}/gpci-{year}.csv")
        repository = self._add_blob_to_repository(blob, MacLocalityRepository())
        if not isinstance(repository, MacLocalityRepository):
            raise ValueError("Incorrect repository type.")
        return repository

    def _add_blob_to_repository(self, blob: Blob, repository: Repository) -> Repository:
        with SpooledTemporaryFile(mode="w") as tmp_file:
            tmp_file.write(blob.download_as_text())
            tmp_file.seek(0)
            repository.add_csv_file(tmp_file)
        return repository
