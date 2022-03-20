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


@dataclass(frozen=True)
class Charge:
    charge_code: str
    modifier: str
    year: int
    description: str
    pw_rvu: float
    non_fac_pe_rvu: float
    fac_pe_rvu: float
    mp_rvu: float
    conv_factor: float

    @classmethod
    def from_dict(cls, dict_: dict[str, str]) -> "Charge":
        return cls(
            charge_code=dict_["charge_code"],
            modifier=dict_["modifier"],
            year=int(dict_["year"]),
            description=dict_["description"],
            pw_rvu=float(dict_["pw_rvu"]),
            non_fac_pe_rvu=float(dict_["non_fac_pe_rvu"]),
            fac_pe_rvu=float(dict_["fac_pe_rvu"]),
            mp_rvu=float(dict_["mp_rvu"]),
            conv_factor=float(dict_["conv_factor"]),
        )


@dataclass(frozen=True)
class Drug:
    charge_code: str
    quarter: int
    year: int
    description: str
    dosage: str
    price: float

    @classmethod
    def from_dict(cls, dict_: dict[str, str]) -> "Drug":
        return cls(
            charge_code=dict_["charge_code"],
            quarter=int(dict_["quarter"]),
            year=int(dict_["year"]),
            description=dict_["description"],
            dosage=dict_["dosage"],
            price=float(dict_["payment_limit"]),
        )


@dataclass(frozen=True)
class Lab:
    charge_code: str
    modifier: str
    year: int
    description: str
    price: float

    @classmethod
    def from_dict(cls, dict_: dict[str, str]) -> "Lab":
        return cls(
            charge_code=dict_["charge_code"],
            modifier=dict_["modifier"],
            year=int(dict_["year"]),
            description=dict_["description"],
            price=float(dict_["payment_limit"]),
        )
