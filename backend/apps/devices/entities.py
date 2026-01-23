from dataclasses import dataclass
from decimal import Decimal

from ninja import Schema

from apps.common.base_entities import BaseEntity
from apps.users.entities import UserEntity


@dataclass
class TypeEntity(BaseEntity):
    name: str


class TypeInputSchema(Schema):
    name: str


@dataclass
class BrandEntity(BaseEntity):
    name: str


class BrandInputSchema(Schema):
    name: str


@dataclass
class DeviceEntity(BaseEntity):
    name: str
    price: Decimal
    img: str | None
    brand: BrandEntity
    type: TypeEntity


class DeviceInputSchema(Schema):
    name: str
    price: Decimal
    brand_id: int
    type_id: int


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
