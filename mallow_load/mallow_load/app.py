from typing import Any, Iterable

from mallow_load.mallow_load.controller.database import ElasticsearchController
from mallow_load.mallow_load.controller.storage import GoogleStorageController
from mallow_load.mallow_load.repository import (
    ChargeRepository,
    DrugRepository,
    LabRepository,
    MacLocalityRepository,
    RepositoryType,
    ZipCodeRepository,
)


class ApplicationService:
    def __init__(self) -> None:
        self.elastic = ElasticsearchController()
        self.google = GoogleStorageController()

    def load_index_for_year(self, index: str, year: int) -> None:
        if index == "gpci_by_zip":
            self._load_gpci_by_zip_index(index, year)
        elif index == "charge":
            self._load_charge_index(index, year)
        else:
            raise ValueError(f"{index} is not a valid index.")

    def _load_gpci_by_zip_index(self, index: str, year: int) -> None:
        zip_repo = self.google.load_zip_code_repository(year)
        mac_locality_repo = self.google.load_mac_locality_repository(year)
        self.elastic.bulk_load_into_index(
            index, self._gen_gpci_documents(index, zip_repo, mac_locality_repo)
        )

    def _load_charge_index(self, index: str, year: int) -> None:
        charge_repo = self.google.load_charge_repository(year)
        lab_repo = self.google.load_lab_repository(year)
        drug_repo = self.google.load_drug_repository(year)
        self.elastic.bulk_load_into_index(
            index, self._gen_charge_documents(index, charge_repo, lab_repo, drug_repo)
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

    def _gen_charge_documents(
        self,
        index: str,
        charge_repo: ChargeRepository,
        lab_repo: LabRepository,
        drug_repo: DrugRepository,
    ) -> Iterable[dict]:
        for charge in charge_repo.repository.values():
            if lab := lab_repo.get((charge.charge_code, charge.modifier)):
                type_ = "LAB"
            elif drug := drug_repo.get((charge.charge_code, 1)):
                type_ = "DRUG"
            else:
                type_ = "STANDARD"
            yield {
                "_index": index,
                "charge_code": charge.charge_code,
                "modifier": charge.modifier,
                "year": charge.year,
                "type": type_,
                "description": charge.description,
                "pw_rvu": charge.pw_rvu,
                "non_fac_pe_rvu": charge.non_fac_pe_rvu,
                "fac_pe_rvu": charge.fac_pe_rvu,
                "mp_rvu": charge.mp_rvu,
                "conv_factor": charge.conv_factor,
                "lab_price": lab.price if lab else None,
                "drug_price_by_quarter": (
                    self._create_drug_price_by_quarter(charge.charge_code, drug_repo)
                    if drug
                    else None
                ),
            }

    def _create_drug_price_by_quarter(
        self, charge_code: str, drug_repo: DrugRepository
    ) -> list[dict[str, Any]]:
        quarters = [1, 2, 3, 4]
        result = []
        for q in quarters:
            if not (drug := drug_repo.get((charge_code, q))):
                continue
            result.append(
                {"quarter": drug.quarter, "dosage": drug.dosage, "price": drug.price}
            )
        return result
