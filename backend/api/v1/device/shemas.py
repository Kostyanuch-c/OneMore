from datetime import datetime
from decimal import Decimal

from ninja import Schema

from apps.devices.entities import (
    BrandEntity,
    DeviceEntity,
    TypeEntity,
)


class BrandOutShema(Schema):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: BrandEntity) -> 'BrandOutShema':
        return BrandOutShema(
            id=entity.id,
            name=entity.name,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class TypeOutShema(Schema):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: TypeEntity) -> 'TypeOutShema':
        return TypeOutShema(
            id=entity.id,
            name=entity.name,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class DeviceOutShema(Schema):
    id: int
    name: str
    price: Decimal
    img: str | None
    brand: BrandOutShema
    type: TypeOutShema
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: DeviceEntity) -> 'DeviceOutShema':
        return DeviceOutShema(
            id=entity.id,
            name=entity.name,
            price=entity.price,
            img=entity.img,
            brand=BrandOutShema.from_entity(entity.brand),
            type=TypeOutShema.from_entity(entity.type),
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
