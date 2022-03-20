import os
from tempfile import SpooledTemporaryFile

from google.cloud import storage
from google.cloud.storage.blob import Blob

from mallow_load.mallow_load.controller.storage.constant import BucketPrefix
from mallow_load.mallow_load.repository import (
    ChargeRepository,
    DrugRepository,
    LabRepository,
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

    def load_charge_repository(self, year: int) -> ChargeRepository:
        blob = self.bucket.get_blob(f"{BucketPrefix.RVU_DATA.value}/rvu-{year}.csv")
        repository = self._add_blob_to_repository(blob, ChargeRepository())
        if not isinstance(repository, ChargeRepository):
            raise ValueError("Incorrect repository type.")
        return repository

    def load_lab_repository(self, year: int) -> LabRepository:
        blob = self.bucket.get_blob(f"{BucketPrefix.LAB_DATA.value}/lab-{year}.csv")
        repository = self._add_blob_to_repository(blob, LabRepository())
        if not isinstance(repository, LabRepository):
            raise ValueError("Incorrect repository type.")
        return repository

    def load_drug_repository(self, year: int) -> DrugRepository:
        repository: Repository = DrugRepository()
        blobs = self.bucket.list_blobs(
            prefix=f"{BucketPrefix.DRUG_DATA.value}/drug-{year}"
        )
        for b in blobs:
            repository = self._add_blob_to_repository(b, repository)
        if not isinstance(repository, DrugRepository):
            raise ValueError("Incorrect repository type.")
        return repository

    def _add_blob_to_repository(self, blob: Blob, repository: Repository) -> Repository:
        with SpooledTemporaryFile(mode="w") as tmp_file:
            tmp_file.write(blob.download_as_text())
            tmp_file.seek(0)
            repository.add_csv_file(tmp_file)
        return repository
