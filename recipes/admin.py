from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from tag.models import Tag

from .models import Category, Recipe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}



@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'is_published', 'created_at', 'author']
    list_display_links = ['title', 'slug']
    list_editable = ['is_published', ]
    prepopulated_fields = {
        'slug': ('title',)
    }
    search_fields = 'id', 'title', 'description', 'slug', 'preparation_steps'
    list_filter = 'category', 'author', 'is_published', 'preparation_steps_is_html'
    list_per_page = 10
    ordering = ('-id',)
    autocomplete_fields = 'tags',
