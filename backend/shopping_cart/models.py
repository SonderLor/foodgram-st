from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class ShoppingCart(models.Model):
    """Модель списка покупок."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name=_("user"),
    )
    recipe = models.ForeignKey(
        "recipes.Recipe",
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name=_("recipe"),
    )

    class Meta:
        verbose_name = _("shopping cart item")
        verbose_name_plural = _("shopping cart items")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_shopping_cart",
            ),
        ]
        indexes = [
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.user} добавил {self.recipe} в список покупок"
