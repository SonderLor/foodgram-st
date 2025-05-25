from rest_framework import serializers

from .models import Subscription
from .serializers import UserWithRecipesSerializer


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""

    class Meta:
        model = Subscription
        fields = ("user", "author")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=("user", "author"),
                message="Вы уже подписаны на этого автора",
            )
        ]

    def validate(self, data):
        if data["user"] == data["author"]:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя"
            )
        return data

    def to_representation(self, instance):
        return UserWithRecipesSerializer(
            instance.author, context={"request": self.context.get("request")}
        ).data
