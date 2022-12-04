from django.urls import path

from . import views

# {% url 'recipes:home' %}
app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/search/', views.search, name='search'),
    path('recipes/<slug:recipe_slug>/', views.recipe, name='recipe'),
    path('recipes/category/<slug:category_slug>/', views.category, name='category'),

]
