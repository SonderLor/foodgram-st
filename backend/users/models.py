from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.constants import (
    MAX_EMAIL_LENGTH,
    MAX_FIRST_NAME_LENGTH,
    MAX_LAST_NAME_LENGTH,
)


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        _("email address"),
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
    )
    first_name = models.CharField(
        _("first name"),
        max_length=MAX_FIRST_NAME_LENGTH,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=MAX_LAST_NAME_LENGTH,
    )
    avatar = models.ImageField(
        _("avatar"),
        upload_to="users/",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("username",)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписок на авторов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name=_("follower"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name=_("author"),
    )

    class Meta:
        verbose_name = _("subscription")
        verbose_name_plural = _("subscriptions")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"],
                name="unique_subscription",
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F("author")),
                name="prevent_self_subscription",
            ),
        ]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["author"]),
        ]

    def __str__(self):
        return f"{self.user} подписан на {self.author}"
