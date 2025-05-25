from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.pagination import CustomPagination
from api.permissions import IsOwnerOrReadOnly
from favorites.models import Favorite
from favorites.serializers import FavoriteSerializer
from shopping_cart.models import ShoppingCart
from shopping_cart.serializers import ShoppingCartSerializer

from .models import Ingredient, Recipe, RecipeIngredient
from .serializers import (
    IngredientSerializer,
    RecipeCreateUpdateSerializer,
    RecipeGetShortLinkSerializer,
    RecipeListSerializer,
)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["^name"]

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__istartswith=name)
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return RecipeCreateUpdateSerializer
        return RecipeListSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()

        author = self.request.query_params.get("author")
        if author:
            queryset = queryset.filter(author_id=author)

        is_favorited = self.request.query_params.get("is_favorited")
        if is_favorited and self.request.user.is_authenticated:
            if is_favorited == "1":
                queryset = queryset.filter(favorites__user=self.request.user)

        is_in_shopping_cart = self.request.query_params.get(
            "is_in_shopping_cart"
        )
        if is_in_shopping_cart and self.request.user.is_authenticated:
            if is_in_shopping_cart == "1":
                queryset = queryset.filter(
                    shopping_cart__user=self.request.user
                )

        return queryset

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[permissions.AllowAny],
        url_path="get-link",
    )
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        serializer = RecipeGetShortLinkSerializer(
            recipe, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        recipe = self.get_object()

        if request.method == "POST":
            serializer = FavoriteSerializer(
                data={"user": request.user.id, "recipe": recipe.id},
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        favorite = get_object_or_404(
            Favorite, user=request.user, recipe=recipe
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()

        if request.method == "POST":
            serializer = ShoppingCartSerializer(
                data={"user": request.user.id, "recipe": recipe.id},
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        cart_item = get_object_or_404(
            ShoppingCart, user=request.user, recipe=recipe
        )
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        # Получаем список ингредиентов пользователя из рецептов в корзине
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shopping_cart__user=request.user
            )
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(total_amount=Sum("amount"))
            .order_by("ingredient__name")
        )

        # Формируем текст списка покупок
        shopping_list = "Список покупок:\n\n"
        for item in ingredients:
            shopping_list += (
                f"{item['ingredient__name']} "
                f"({item['ingredient__measurement_unit']}) — "
                f"{item['total_amount']}\n"
            )

        response = HttpResponse(shopping_list, content_type="text/plain")
        response["Content-Disposition"] = (
            'attachment; filename="shopping_list.txt"'
        )
        return response
