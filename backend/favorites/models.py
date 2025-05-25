from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Favorite(models.Model):
    """Модель избранных рецептов."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name=_("user"),
    )
    recipe = models.ForeignKey(
        "recipes.Recipe",
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name=_("recipe"),
    )

    class Meta:
        verbose_name = _("favorite")
        verbose_name_plural = _("favorites")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_favorite",
            ),
        ]
        indexes = [
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.user} добавил {self.recipe} в избранное"
