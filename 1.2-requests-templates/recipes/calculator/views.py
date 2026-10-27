from django.http import HttpResponse
from django.shortcuts import render, reverse

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


def get_request_data(request, recipe_type):
    try:
        servings = int(request.GET.get('servings'))
    except:
        servings = 1
    data = {}
    for key, value in DATA[recipe_type].items():
        data[key] = value*servings
    return data


def omlet(request):
    data = get_request_data(request, 'omlet')
    return render(request, 'calculator/index.html', {'recipe': data})


def pasta(request):
    data = get_request_data(request, 'pasta')
    return render(request, 'calculator/index.html', {'recipe': data})


def buter(request):
    data = get_request_data(request, 'buter')
    return render(request, 'calculator/index.html', {'recipe': data})

