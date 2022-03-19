from enum import Enum


class BucketPrefix(Enum):
    GPCI_DATA = "gpci-data"
    DRUG_DATA = "drug-data"
    LAB_DATA = "lab-data"
    RVU_DATA = "rvu-data"
    ZIP_DATA = "zip-data"
