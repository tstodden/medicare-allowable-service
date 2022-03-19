from typing import Any

from mallow_load.mallow_load.error import MappingDoesNotExistError

_GPCI_BY_ZIP_MAPPING = {
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

_MAPPING_TO_INDEX = {
    "gpci_by_zip": _GPCI_BY_ZIP_MAPPING,
}


def get_mapping_by_index(index: str) -> dict[str, Any]:
    try:
        return _MAPPING_TO_INDEX[index]
    except KeyError:
        raise MappingDoesNotExistError(f"A mapping for {index} does not exist.")
