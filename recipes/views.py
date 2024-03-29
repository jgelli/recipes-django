import os

from django.contrib import messages
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import DetailView, ListView

from utils.pagination import make_pagination

from .models import Recipe
from tag.models import Tag

PER_PAGE = os.environ.get('PER_PAGE', 9)


class RecipeListViewBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            is_published=True,
        )
        query_set = query_set.select_related('author', 'category')
        query_set = query_set.prefetch_related('tags')
        return query_set

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(self.request, context.get('recipes'), PER_PAGE)

        context.update({
            'recipes': page_obj,
            'pagination_range': pagination_range,
        })
        return context


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            category__slug=self.kwargs.get('category_slug'),
        )

        if not query_set:
            raise Http404()

        return query_set

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': f'{context.get("recipes")[0].category.name} - Category Recipes '
        })
        return context


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            ),
        )

        return query_set

    def get_context_data(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'page_title': f'Search for "{search_term}"',
            'q': search_term,
            'additional_url_query': f'&q={search_term}'
        })
        return context

class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(tags__slug=self.kwargs.get('slug', ''))

        return query_set

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(slug=self.kwargs.get('slug', '')).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag'

        context.update({
            'page_title': page_title,
        })
        return context


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/details.html'

    def get_object(self):
        slug = self.kwargs.get('recipe_slug')
        return get_object_or_404(
            Recipe,
            slug=slug,
            is_published=True
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'is_detail_page': True,
        })
        return context
