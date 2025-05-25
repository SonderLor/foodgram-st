from django.shortcuts import get_object_or_404, redirect

from recipes.models import Recipe


def recipe_short_link_redirect(request, short_link):
    """Редирект с короткой ссылки на страницу рецепта."""
    recipe = get_object_or_404(Recipe, short_link=short_link)
    return redirect(f"/recipes/{recipe.id}/")
