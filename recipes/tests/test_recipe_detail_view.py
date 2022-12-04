from django.urls import resolve, reverse
from django.utils.text import slugify

from recipes import views

from .test_recipe_base import RecipeTestBase

NOT_FOUND_CODE = 404


class RecipeDetailViewTest(RecipeTestBase):

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'recipe_slug': 'pizza-de-forno'}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'recipe_slug': 'non-existent-recipe'}))
        self.assertEqual(response.status_code, NOT_FOUND_CODE)

    def test_recipe_detail_template_loads_recipes(self):
        recipe_title = 'Cheese Pizza'
        recipe_slug = slugify(recipe_title)

        self.make_recipe(
            title=recipe_title,
            slug=recipe_slug
        )
        response = self.client.get(reverse('recipes:recipe', kwargs={'recipe_slug': recipe_slug}))
        content = response.content.decode('utf-8')
        self.assertIn(recipe_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        recipe_title = 'Cheese Pizza'
        recipe_slug = slugify(recipe_title)

        self.make_recipe(
            title=recipe_title,
            slug=recipe_slug,
            is_published=False
        )
        response = self.client.get(reverse('recipes:recipe', kwargs={'recipe_slug': recipe_slug}))
        self.assertEqual(response.status_code, NOT_FOUND_CODE)
