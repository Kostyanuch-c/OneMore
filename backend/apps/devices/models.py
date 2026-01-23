from django.db import models

from apps.common.models import BaseTimedModel
from myproject.settings import AUTH_USER_MODEL


class Type(BaseTimedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "device_types"
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Brand(BaseTimedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "device_brands"
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Rating(BaseTimedModel):
    rate = models.PositiveSmallIntegerField()
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    device = models.ForeignKey(
        "Device",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return str(self.rate)

    class Meta:
        db_table = "device_ratings"
        default_related_name = "ratings"
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'device'], name='unique_user_device_rating'
            )
        ]


class DeviceInfo(BaseTimedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    device = models.ForeignKey(
        'Device',
        on_delete=models.CASCADE,
        related_name="infos",
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
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.PROTECT,
    )

    def __str__(self) -> str:
        return f"{self.name} - ${self.price:.2f}"

    class Meta:
        default_related_name = "devices"
        db_table = "device"
        verbose_name = 'Девайс'
        verbose_name_plural = 'Девайсы'
