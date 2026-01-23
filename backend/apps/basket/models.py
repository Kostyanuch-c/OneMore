from django.db import models

from apps.common.models import BaseTimedModel
from apps.devices.models import Device
from myproject.settings import AUTH_USER_MODEL


class Basket(BaseTimedModel):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=False)
    devices: "models.ManyToManyField[Device, BasketItem]" = (
        models.ManyToManyField(
            Device,
            through='BasketItem',
        )
    )

    class Meta:
        default_related_name = 'baskets'
        db_table = 'basket'
        ordering = ['-created_at']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self) -> str:
        return (
            f"Basket {self.id} for {self.user.username}"
            f" (active: {self.is_active})"
        )


class BasketItem(BaseTimedModel):
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
        related_name='items',
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='devices_in_basket',
    )
    quantity = models.PositiveIntegerField(default=1)
    price_at_added = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'basket_item'
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['basket', 'device'], name='unique_basket_device'
            )
        ]

    def __str__(self) -> str:
        return (
            f"{self.device.name} x {self.quantity} in Basket {self.basket.id}"
        )
