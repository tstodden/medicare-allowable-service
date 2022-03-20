from typing import Any

from mallow_load.mallow_load.error import MappingDoesNotExistError

_GPCI_BY_ZIP_MAPPING: dict[str, Any] = {
    "properties": {
        "zip_code": {
            "type": "text",
        },
        "year": {
            "type": "short",
        },
        "mac_id": {
            "type": "short",
        },
        "locality_id": {
            "type": "short",
        },
        "pw_gpci": {
            "type": "float",
        },
        "pe_gpci": {
            "type": "float",
        },
        "mp_gpci": {
            "type": "float",
        },
    }
}

_CHARGE_MAPPING: dict[str, Any] = {
    "properties": {
        "charge_code": {
            "type": "text",
        },
        "modifier": {
            "type": "text",
        },
        "year": {
            "type": "short",
        },
        "type": {
            "type": "text",
        },
        "description": {
            "type": "text",
        },
        "pw_rvu": {
            "type": "float",
        },
        "non_fac_pe_rvu": {
            "type": "float",
        },
        "fac_pe_rvu": {
            "type": "float",
        },
        "mp_rvu": {
            "type": "float",
        },
        "conv_factor": {
            "type": "float",
        },
        "lab_price": {
            "type": "float",
        },
        "drug_price_by_quarter": {
            "type": "nested",
            "properties": {
                "quarter": {
                    "type": "byte",
                },
                "dosage": {
                    "type": "text",
                },
                "price": {
                    "type": "float",
                },
            },
        },
    }
}

_MAPPING_TO_INDEX = {
    "gpci_by_zip": _GPCI_BY_ZIP_MAPPING,
    "charge": _CHARGE_MAPPING,
}


def get_mapping_by_index(index: str) -> dict[str, Any]:
    try:
        return _MAPPING_TO_INDEX[index]
    except KeyError:
        raise MappingDoesNotExistError(f"A mapping for {index} does not exist.")
