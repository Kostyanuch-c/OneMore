from decimal import Decimal

from ninja import UploadedFile

from apps.devices.entities import (
    BrandEntity,
    DeviceEntity,
    TypeEntity,
)
from apps.devices.models import (
    Brand,
    Device,
    Type,
)


def brand_converter(brand_instance: Brand) -> BrandEntity:
    return BrandEntity(
        id=brand_instance.id,
        name=brand_instance.name,
        created_at=brand_instance.created_at,
        updated_at=brand_instance.updated_at,
    )


class BrandService:
    brand_model = Brand

    def create_brand(self, name: str) -> BrandEntity:
        return brand_converter(self.brand_model.objects.create(name=name))

    def get_list_brands(self) -> list[BrandEntity]:
        return [brand_converter(obj) for obj in self.brand_model.objects.all()]


def type_converter(type_instance: Type) -> TypeEntity:
    return TypeEntity(
        id=type_instance.id,
        name=type_instance.name,
        created_at=type_instance.created_at,
        updated_at=type_instance.updated_at,
    )


class TypeService:
    type_model = Type

    def create_type(self, name: str) -> TypeEntity:
        return type_converter(self.type_model.objects.create(name=name))

    def get_list_types(self) -> list[TypeEntity]:
        return [type_converter(obj) for obj in self.type_model.objects.all()]


def device_converter(device_instance: Device) -> DeviceEntity:
    return DeviceEntity(
        id=device_instance.id,
        name=device_instance.name,
        price=device_instance.price,
        img=device_instance.img.url,
        brand=brand_converter(device_instance.brand),
        type=type_converter(device_instance.type),
        created_at=device_instance.created_at,
        updated_at=device_instance.updated_at,
    )


class DeviceService:
    device_model = Device

    def create_device(
        self,
        name: str,
        price: Decimal,
        brand_id: int,
        type_id: int,
        img_file: UploadedFile | None = None,
    ) -> DeviceEntity:
        return device_converter(
            self.device_model.objects.create(
                name=name,
                price=price,
                brand_id=brand_id,
                type_id=type_id,
                img=img_file,
            )
        )

    def get_list_devices(self) -> list[DeviceEntity]:
        return [device_converter(obj) for obj in self.device_model.objects.all()]
