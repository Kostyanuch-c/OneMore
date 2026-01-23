from dataclasses import dataclass
from decimal import Decimal

from apps.common.base_entities import BaseEntity
from apps.devices.entities import DeviceEntity
from apps.users.entities import UserEntity


@dataclass
class BasketEntity(BaseEntity):
    user: UserEntity
    is_active: bool
    items: list["BasketItemEntity"]


@dataclass
class BasketItemEntity(BaseEntity):
    device: DeviceEntity
    quantity: int
    price_to_added: Decimal
