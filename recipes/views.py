import os

from django.contrib import messages
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.pagination import make_pagination

from .models import Recipe

PER_PAGE = os.environ.get('PER_PAGE', 9)


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    context = {
        'recipes': page_obj,
        'pagination_range': pagination_range
    }

    return render(request, 'recipes/pages/home.html', context=context)


def recipe(request, recipe_slug):
    recipe = get_object_or_404(
        Recipe.objects.filter(slug=recipe_slug, is_published=True)
    )

    context = {
        'recipe': recipe,
        'is_detail_page': True,
    }
    return render(request, 'recipes/pages/details.html', context=context)


def category(request, category_slug):

    recipes = get_list_or_404(
        Recipe.objects.filter(category__slug=category_slug, is_published=True).order_by('-id')
    )

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    context = {
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'{recipes[0].category.name} - Category Recipes '
    }

    return render(request, 'recipes/pages/category.html', context=context)


def search(request):
    q = request.GET.get('q', '').strip()

    if not q:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=q) | 
            Q(title__icontains=q),
        ),
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    context = {
        'page_title': f'Search for "{q}"',
        'q': q,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={q}'
    }

    return render(request, 'recipes/pages/search.html', context=context)
