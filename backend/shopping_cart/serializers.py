from rest_framework import serializers

from core.common_serializers import RecipeMinifiedSerializer
from .models import ShoppingCart


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для списка покупок."""

    class Meta:
        model = ShoppingCart
        fields = ("user", "recipe")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=("user", "recipe"),
                message="Рецепт уже в списке покупок",
            )
        ]

    def to_representation(self, instance):
        return RecipeMinifiedSerializer(
            instance.recipe, context={"request": self.context.get("request")}
        ).data
