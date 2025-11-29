from django.db import models

from apps.common.models import BaseTimedModel


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

    def __str__(self) -> str:
        return f'rating {self.rate}'

    class Meta:
        db_table = "device_ratings"
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class DeviceInfo(BaseTimedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self) -> str:
        return f'Описание устройства {self.title}'

    class Meta:
        db_table = "device_info"
        verbose_name = 'Информация о устройстве'


class Device(BaseTimedModel):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.ForeignKey(
        Rating,
        on_delete=models.CASCADE,
        related_name='device_as_rating',
    )
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
    device_info = models.ManyToManyField(DeviceInfo, related_name='devices')

    def __str__(self) -> str:
        return f"{self.name} - ${self.price:.2f}"

    class Meta:
        db_table = "device"
        verbose_name = 'Девайс'
        verbose_name_plural = 'Девайсы'
