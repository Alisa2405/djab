pythifrom django.shortcuts import render

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

def recipe_view(request, dish):
    # получаем servings из GET, по умолчанию 1
    servings = request.GET.get('servings', 1)
    servings = int(servings)

    # берём рецепт
    recipe = DATA.get(dish)

    # если рецепт найден — считаем ингредиенты
    if recipe:
        recipe = {
            ingredient: amount * servings
            for ingredient, amount in recipe.items()
        }

    context = {
        'recipe': {
            'ингредиент1': количество1,
            'ингредиент2': количество2,
        }
    }

    return render(request, 'calculator/index.html', context)