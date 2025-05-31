from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from .models import Recipe


class IngredientFilter(SearchFilter):
    """Фильтр для поиска ингредиентов по названию."""

    search_param = "name"

    def get_search_fields(self, view, request):
        return ["name"]

    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get(self.search_param)
        if name:
            return queryset.filter(name__startswith=name)
        return queryset


class RecipeFilter(filters.FilterSet):
    """Фильтр для рецептов."""

    is_favorited = filters.BooleanFilter(method="filter_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method="filter_is_in_shopping_cart"
    )
    author = filters.NumberFilter(field_name="author__id")

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping_cart__user=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ["author", "is_favorited", "is_in_shopping_cart"]
