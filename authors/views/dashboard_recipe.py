from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from authors.forms.recipe import AuthorRecipeForm
from recipes.models import Recipe


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipe(View):
    def get_recipe(self, slug=None):
        recipe = None

        if slug:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                slug=slug
            ).first()

            if not recipe:
                raise Http404()

        return recipe

    def render_recipe(self, form):
        return render(
            self.request,
            'authors/pages/dashboard_recipe.html',
            context={
                'form': form
            })

    def get(self, request, slug=None):
        recipe = self.get_recipe(slug)

        form = AuthorRecipeForm(instance=recipe)

        return self.render_recipe(form)

    def post(self, request, slug=None):
        recipe = self.get_recipe(slug)

        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()
            messages.success(request, 'Your recipe is successfully saved!')
            return redirect('authors:dashboard_recipe_edit', recipe.slug)

        return self.render_recipe(form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, request):
        slug = self.request.POST.get('slug')
        recipe = self.get_recipe(slug)
        recipe.delete()
        messages.success(request, 'Deleted successfully!')
        return redirect('authors:dashboard')
