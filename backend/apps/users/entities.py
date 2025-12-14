from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from ninja import Schema

from apps.common.base_entities import BaseEntity


if TYPE_CHECKING:
    from apps.devices.entities import DeviceEntity


@dataclass
class UserEntity:
    id: int
    username: str
    first_name: str | None
    last_name: str | None
    full_name: str | None
    created_at: datetime


class UserInputSchema(Schema):
    password: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    username: str


class UserUpdateSchema(Schema):
    username: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None


@dataclass
class BasketEntity(BaseEntity):
    user: UserEntity
    is_active: bool
    item: list["BasketItemEntity"]


@dataclass
class BasketItemEntity(BaseEntity):
    device: "DeviceEntity"
    quantity: int
    price_to_added: Decimal
