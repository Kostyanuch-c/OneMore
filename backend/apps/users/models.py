from django.contrib.auth import get_user_model
from django.db import models

from apps.common.models import BaseTimedModel
from apps.devices.models import Device


class Basket(BaseTimedModel):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='user_as_basket',
    )
    is_active = models.BooleanField(default=False)
    devices: "models.ManyToManyField[Device, BasketDevice]" = (
        models.ManyToManyField(
            Device,
            through='BasketDevice',
            related_name='baskets',
        )
    )

    class Meta:
        db_table = 'user_basket'
        ordering = ['-created_at']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self) -> str:
        return (
            f"Basket {self.id} for {self.user.username}"
            f" (active: {self.is_active})"
        )


class BasketDevice(BaseTimedModel):
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
        related_name='items',
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='basket_entries',
    )
    quantity = models.PositiveIntegerField(default=1)
    price_at_added = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return (
            f"{self.device.name} x {self.quantity} in Basket {self.basket.id}"
        )

    class Meta:
        db_table = 'user_basket_device'
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
