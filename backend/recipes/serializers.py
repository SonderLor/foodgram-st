from django.db import transaction
from rest_framework import serializers

from core.fields import Base64ImageField
from core.constants import MIN_AMOUNT_OF_INGREDIENT, MIN_COOKING_TIME
from users.serializers import CustomUserSerializer
from .models import Ingredient, Recipe, RecipeIngredient


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов в рецепте."""

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка рецептов."""

    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source="recipe_ingredients", many=True, read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()


class IngredientCreateSerializer(serializers.Serializer):
    """Сериализатор для добавления ингредиентов при создании рецепта."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=MIN_AMOUNT_OF_INGREDIENT)

    def validate_amount(self, value):
        if value < MIN_AMOUNT_OF_INGREDIENT:
            raise serializers.ValidationError(
                "Количество ингредиента должно быть не меньше "
                f"{MIN_AMOUNT_OF_INGREDIENT}"
            )
        return value


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления рецепта."""

    ingredients = IngredientCreateSerializer(many=True)
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def validate(self, data):
        if "ingredients" not in self.initial_data:
            raise serializers.ValidationError(
                {"ingredients": "Поле ингредиентов обязательно"}
            )
        return super().validate(data)

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError("Нужен хотя бы один ингредиент")

        ingredient_ids = [item["id"].id for item in value]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                "Ингредиенты не должны повторяться"
            )

        return value

    def validate_cooking_time(self, value):
        if value < MIN_COOKING_TIME:
            raise serializers.ValidationError(
                f"Время приготовления должно быть не меньше {MIN_COOKING_TIME}"
            )
        return value

    def create_ingredients(self, recipe, ingredients):
        RecipeIngredient.objects.bulk_create(
            [
                RecipeIngredient(
                    recipe=recipe,
                    ingredient_id=ingredient["id"].id,
                    amount=ingredient["amount"],
                )
                for ingredient in ingredients
            ]
        )

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(
            author=self.context.get("request").user, **validated_data
        )
        self.create_ingredients(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients", None)

        instance.recipe_ingredients.all().delete()
        self.create_ingredients(instance, ingredients)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeListSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class RecipeGetShortLinkSerializer(serializers.ModelSerializer):
    """Сериализатор для получения короткой ссылки на рецепт."""

    short_link = serializers.SerializerMethodField(
        method_name="get_short_link"
    )

    class Meta:
        model = Recipe
        fields = ("short_link",)

    def get_short_link(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(f"/s/{obj.short_link}")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["short-link"] = data.pop("short_link")
        return data
