from dataclasses import dataclass
from decimal import Decimal

from apps.common.base_entities import BaseEntity
from apps.users.entities import UserEntity


@dataclass
class TypeEntity(BaseEntity):
    name: str


@dataclass
class BrandEntity(BaseEntity):
    name: str


@dataclass
class DeviceEntity(BaseEntity):
    name: str
    price: Decimal
    img: str
    brand: BrandEntity
    type: TypeEntity


@dataclass
class RatingEntity(BaseEntity):
    rate: int | float
    user: UserEntity
    device: DeviceEntity


@dataclass
class DeviceInfoEntity(BaseEntity):
    title: str
    description: str
    device: DeviceEntity
