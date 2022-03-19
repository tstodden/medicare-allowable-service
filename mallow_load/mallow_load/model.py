from dataclasses import dataclass


@dataclass(frozen=True)
class ZipCode:
    zip_code: str
    year: int
    mac_id: int
    locality_id: int

    @classmethod
    def from_dict(cls, dict_: dict[str, str]) -> "ZipCode":
        return cls(
            zip_code=dict_["zip_code"],
            year=int(dict_["year"]),
            mac_id=int(dict_["carrier_id"]),
            locality_id=int(dict_["locality_id"]),
        )


@dataclass(frozen=True)
class MacLocality:
    mac_id: int
    locality_id: int
    year: int
    locality_name: str
    pw_gpci: float
    pe_gpci: float
    mp_gpci: float

    @classmethod
    def from_dict(cls, dict_: dict[str, str]) -> "MacLocality":
        return cls(
            mac_id=int(dict_["mac_id"]),
            locality_id=int(dict_["locality_id"]),
            year=int(dict_["year"]),
            locality_name=dict_["locality_name"],
            pw_gpci=float(dict_["pw_gpci"]),
            pe_gpci=float(dict_["pe_gpci"]),
            mp_gpci=float(dict_["mp_gpci"]),
        )
