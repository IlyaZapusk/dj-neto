from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
from django.views import View
from django.http import JsonResponse, HttpResponse


def recipe_view(request, dish):
    servings = request.GET.get('servings', 1)
    try:
        servings = int(servings)
    except ValueError:
        servings = 1  # Защита от неправильного ввода

    recipe = DATA.get(dish)
    if recipe is None:
        return HttpResponse(f"Рецепт '{dish}' не найден.", status=404)

    scaled_recipe = {ingredient: round(quantity * servings, 2) for ingredient, quantity in recipe.items()}

    context = {
        'recipe': scaled_recipe
    }
    return render(request, 'calculator/index.html', context)