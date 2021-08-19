import json

from django.shortcuts import (
    render,
)
from django.views import (
    View,
)

from recipes.models import Recipe, UserRecipe
from users.models import CustomUser


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

        data = {
            'response': users_recipes_dict,
        }

        result = json.dumps(
            data,
            sort_keys=False,
            indent=4,
            ensure_ascii=False,
            separators=(',', ': ')
        )
        return render(request, 'task.html', {'json_data': result})


class Task2View(View):
    """
    Вывести детальную информацию рецепта. Нужно получить информацию о самом рецепте, о шагах приготовления, списке
    необходимых продоктов для приготовления
    """

    def get(self, request, **kwargs):
        data = {
            'response': 'some data task 2',
        }

        return render(request, 'task.html', {'json_data': json.dumps(data)})


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



