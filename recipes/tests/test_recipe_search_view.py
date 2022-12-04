from unittest.mock import patch

from django.urls import resolve, reverse
from django.utils.text import slugify

from recipes import views

from .test_recipe_base import RecipeTestBase

NOT_FOUND_CODE = 404


class RecipeSearchViewTest(RecipeTestBase):

    def teste_recipe_search_uses_correct_view_function(self):
        search_url = reverse('recipes:search')
        resolved = resolve(search_url)
        self.assertEqual(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=test')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, NOT_FOUND_CODE)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        response = self.client.get(reverse('recipes:search') + '?q=Teste')
        content = response.content.decode('utf-8')
        self.assertIn(
            'Search for &quot;Teste&quot;',
            content
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        recipe_title1 = 'This is recipe one'
        recipe_title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            title=recipe_title1,
            slug=slugify(recipe_title1),
            author_data={'username': 'one'},
            category_data={
                'slug': 'a'
            }
        )
        recipe2 = self.make_recipe(
            title=recipe_title2,
            slug=slugify(recipe_title2),
            author_data={'username': 'two'},
            category_data={
                'slug': 'b'
            }
        )

        search_url = reverse('recipes:search')

        response1 = self.client.get(f'{search_url}?q={recipe_title1}')
        response2 = self.client.get(f'{search_url}?q={recipe_title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        context1 = response1.context['recipes']
        context2 = response2.context['recipes']
        context_both = response_both.context['recipes']

        self.assertIn(recipe1, context1)
        self.assertNotIn(recipe2, context1)

        self.assertIn(recipe2, context2)
        self.assertNotIn(recipe1, context2)

        self.assertIn(recipe1, context_both)
        self.assertIn(recipe2, context_both)

    def test_recipe_search_is_paginated(self):
        recipe_title = 'Recipe'
        for i in range(9):
            kwargs = {
                'author_data': {'username': f'u{i}'},
                'category_data': {'slug': f'slug{i}'},
                'slug': f'recipe-{i}',
                'title': f'{recipe_title} {i}'
            }
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            search_url = reverse('recipes:search')

            response = self.client.get(f'{search_url}?q={recipe_title}')
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 3)
