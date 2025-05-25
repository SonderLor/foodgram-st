import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        _("name"),
        max_length=128,
    )
    measurement_unit = models.CharField(
        _("measurement unit"),
        max_length=64,
    )

    class Meta:
        verbose_name = _("ingredient")
        verbose_name_plural = _("ingredients")
        ordering = ("name",)
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name=_("author"),
    )
    name = models.CharField(
        _("name"),
        max_length=256,
    )
    image = models.ImageField(
        _("image"),
        upload_to="recipes/",
    )
    text = models.TextField(
        _("description"),
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes",
        verbose_name=_("ingredients"),
    )
    cooking_time = models.PositiveIntegerField(
        _("cooking time"),
    )
    pub_date = models.DateTimeField(
        _("publication date"),
        auto_now_add=True,
    )
    short_link = models.CharField(
        _("short link"),
        max_length=10,
        unique=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("recipe")
        verbose_name_plural = _("recipes")
        ordering = ("-pub_date",)

    def save(self, *args, **kwargs):
        if not self.short_link:
            self.short_link = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель для связи рецепта и ингредиентов с указанием количества."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
        verbose_name=_("recipe"),
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
        verbose_name=_("ingredient"),
    )
    amount = models.PositiveIntegerField(
        _("amount"),
    )

    class Meta:
        verbose_name = _("recipe ingredient")
        verbose_name_plural = _("recipe ingredients")
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            ),
        ]
        indexes = [
            models.Index(fields=["recipe"]),
            models.Index(fields=["ingredient"]),
        ]

    def __str__(self):
        return f"{self.recipe.name}: {self.ingredient.name} - {self.amount}"
