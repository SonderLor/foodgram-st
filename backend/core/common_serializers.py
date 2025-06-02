from rest_framework import serializers

from recipes.models import Recipe


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    """Сериализатор для краткого представления рецепта."""

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
        read_only_fields = ("id", "name", "image", "cooking_time")
