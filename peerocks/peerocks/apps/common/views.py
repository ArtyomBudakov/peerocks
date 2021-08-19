import json

from django.shortcuts import (
    render,
)
from django.views import (
    View,
)

from recipes.models import Recipe, UserRecipe, CookStep, CookStepRecipeProduct, RecipeProduct
from users.models import CustomUser


def packing(dict_for_packing: dict) -> str:
    """
    Из Dict с кириллицей формирует Json в формате str для вывода на сайт
    """
    packed_dict = json.dumps(
        {'response': dict_for_packing},
        sort_keys=False,
        indent=4,
        ensure_ascii=False,
        separators=(',', ': ')
    )
    return packed_dict


class Task1View(View):
    """
    Вывести список всех рецептов. Список должен содержать информацию о самом рецепте, авторе
    """

    def get(self, request, **kwargs):
        users_recipes_queryset = UserRecipe.objects.all()

        users_recipes_dict: dict = {}
        row_number_generator = (number for number in range(0, users_recipes_queryset.count()))

        for user_recipe_queryset in users_recipes_queryset:
            user_recipe_dict = {
                "user": str(user_recipe_queryset.user),
                "recipe": user_recipe_queryset.recipe.title,
                "description": user_recipe_queryset.recipe.description
            }
            row_number = str(next(row_number_generator))
            users_recipes_dict[row_number] = user_recipe_dict

        result = packing(users_recipes_dict)
        return render(request, 'task.html', {'json_data': result})


class Task2View(View):
    """
    Вывести детальную информацию рецепта. Нужно получить информацию о самом рецепте,
    о шагах приготовления, списке необходимых продуктов для приготовления
    """

    def get(self, request, **kwargs):
        recipe_products_steps: dict = {}

        some_recipe = Recipe.objects.first()
        recipe_products_steps[some_recipe.title] = {"описание": some_recipe.description}

        recipe_products = RecipeProduct.objects.filter(recipe=some_recipe)
        recipe_products_steps[some_recipe.title]["продукты"] = []
        for item in recipe_products:
            recipe_products_steps[some_recipe.title]["продукты"].append(item.product.title)

        cook_steps = CookStep.objects.\
            filter(recipe=some_recipe).\
            values('title', 'description').\
            distinct()
        recipe_products_steps[some_recipe.title]["шаги"] = {}

        for item in cook_steps:
            recipe_products_steps[some_recipe.title]["шаги"].update({item['title']: item['description']})

        result = packing(recipe_products_steps)
        return render(request, 'task.html', {'json_data': result})


class Task3View(View):
    """
    Вывести список рецептов, аналогичный заданию 1, только дополнительно должно быть выведено количество лайков. Сам
    список должен быть отсортирован по количеству лайков по убыванию
    """

    def get(self, request, **kwargs):
        data = {
            'response': 'some data task 3',
        }

        return render(request, 'task.html', {'json_data': json.dumps(data)})


class Task4View(View):
    """
    Вывести объединенный список TOP 3 авторов и TOP 3 голосующих с количеством рецептов для первых и количеством
    голосов для вторых. В выборке должен быть указан тип в отдельной колонкке - Автор или Пользователь.
    """

    def get(self, request, **kwargs):
        data = {
            'response': 'some data task 4',
        }

        return render(request, 'task.html', {'json_data': json.dumps(data)})


class Task5View(View):
    """
    Все продукты указаны для приготовления одной порции блюда. Необходимо вывести список необходимых продуктов для
    приготовления самостоятельно выбранного блюда в количестве 5-ти порций
    """

    def get(self, request, **kwargs):
        data = {
            'response': 'some data task 5',
        }

        return render(request, 'task.html', {'json_data': json.dumps(data)})



