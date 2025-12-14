from django.db import models

from apps.common.models import BaseTimedModel
from apps.devices.entities import (
    BrandEntity,
    DeviceEntity,
    DeviceInfoEntity,
    TypeEntity,
)
from myproject.settings import AUTH_USER_MODEL


class Type(BaseTimedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    def to_entity(self) -> TypeEntity:
        return TypeEntity(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    class Meta:
        db_table = "device_types"
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Brand(BaseTimedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    def to_entity(self) -> BrandEntity:
        return BrandEntity(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    class Meta:
        db_table = "device_brands"
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Rating(BaseTimedModel):
    rate = models.PositiveSmallIntegerField()
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    device = models.ForeignKey(
        "Device",
        on_delete=models.CASCADE,
        related_name="ratings",
    )

    # def to_entity(self) -> RatingEntity:
    #     return RatingEntity(
    #         id=self.id,
    #         rate=self.rate,
    #         user=self.user.to_entity(),
    #         device=self.device.to_entity(),
    #         created_at=self.created_at,
    #         updated_at=self.updated_at,
    #     )

    def __str__(self) -> str:
        return str(self.rate)

    class Meta:
        db_table = "device_ratings"
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
        unique_together = ("user", "device")


class DeviceInfo(BaseTimedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    device = models.ForeignKey(
        'Device',
        on_delete=models.CASCADE,
        related_name="infos",
    )

    def to_entity(self) -> DeviceInfoEntity:
        return DeviceInfoEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            device=self.device.to_entity(),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self) -> str:
        return f'Описание устройства {self.title}'

    class Meta:
        db_table = "device_info"
        verbose_name = 'Информация о устройстве'


class Device(BaseTimedModel):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    img = models.ImageField(upload_to="devices/img", null=True, blank=True)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name='device_as_brand',
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.PROTECT,
        related_name='device_as_type',
    )

    def to_entity(self) -> DeviceEntity:
        return DeviceEntity(
            id=self.id,
            name=self.name,
            price=self.price,
            img=self.img,
            type=self.type.to_entity(),
            brand=self.brand.to_entity(),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self) -> str:
        return f"{self.name} - ${self.price:.2f}"

    class Meta:
        db_table = "device"
        verbose_name = 'Девайс'
        verbose_name_plural = 'Девайсы'
