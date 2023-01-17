from django.urls import path

from . import views

# {% url 'recipes:home' %}
app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),
    path('recipes/<slug:recipe_slug>/', views.RecipeDetail.as_view(), name='recipe'),
    path('recipes/category/<slug:category_slug>/', views.RecipeListViewCategory.as_view(), name='category'),

]
