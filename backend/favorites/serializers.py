from rest_framework import serializers

from recipes.serializers import RecipeMinifiedSerializer
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов."""

    class Meta:
        model = Favorite
        fields = ("user", "recipe")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=("user", "recipe"),
                message="Рецепт уже в избранном",
            )
        ]

    def to_representation(self, instance):
        return RecipeMinifiedSerializer(
            instance.recipe, context={"request": self.context.get("request")}
        ).data
