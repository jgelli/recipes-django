from unittest.mock import patch

from django.urls import resolve, reverse
from django.utils.text import slugify

from recipes import views

from .test_recipe_base import RecipeTestBase

NOT_FOUND_CODE = 404


class RecipeCategoryViewTest(RecipeTestBase):

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_slug': 'pizza'}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_slug': 'non-existent-category'}))
        self.assertEqual(response.status_code, NOT_FOUND_CODE)

    def test_recipe_category_template_loads_recipes(self):
        recipe_title = 'Cheese Pizza'
        category_title = 'Pizza'
        category_slug = slugify(category_title)

        self.make_recipe(
            title=recipe_title,
            category_data={
                'name': category_title,
                'slug': category_slug
            }
        )
        response = self.client.get(reverse('recipes:category', kwargs={'category_slug': category_slug}))
        content = response.content.decode('utf-8')
        self.assertIn(category_title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe_title = 'Cheese Pizza'
        category_title = 'Pizza'
        category_slug = slugify(category_title)

        self.make_recipe(
            title=recipe_title,
            is_published=False,
            category_data={
                'name': category_title,
                'slug': category_slug
            }
        )
        response = self.client.get(reverse('recipes:category', kwargs={'category_slug': category_slug}))
        self.assertEqual(response.status_code, NOT_FOUND_CODE)

    def test_recipe_category_is_paginated(self):
        # recipe with diff category
        self.make_recipe()

        category = self.make_category(slug='slug-test')
        for i in range(3):
            kwargs = {
                'author_data': {'username': f'u{i}'},
                'category': category,
                'slug': f'recipe-{i}'
            }
            self.make_recipe_with_category(**kwargs)

        with patch('recipes.views.PER_PAGE', new=1):
            response = self.client.get(reverse('recipes:category', kwargs={'category_slug': category.slug}))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 1)
            self.assertEqual(len(paginator.get_page(2)), 1)
            self.assertEqual(len(paginator.get_page(3)), 1)
