from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "get_favorites_count")
    search_fields = ("name", "author__username")
    list_filter = ("author", "name")
    inlines = (RecipeIngredientInline,)
    readonly_fields = ("get_favorites_count",)

    def get_favorites_count(self, obj):
        return obj.favorites.count()

    get_favorites_count.short_description = "В избранном"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("measurement_unit",)
