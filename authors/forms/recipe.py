from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = (
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            'cover',
        )
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Portion', 'Portion'),
                    ('Pieces', 'Pieces'),
                    ('People', 'People'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutes', 'Minutes'),
                    ('Hours', 'Hours'),
                )
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        preparation_time = cleaned_data.get('preparation_time')
        servings = cleaned_data.get('servings')

        if len(title) < 5:
            self._my_errors['title'].append('Must have at least 5 letters.')

        if not is_positive_number(preparation_time):
            self._my_errors['preparation_time'].append('Must be greater than zero.')

        if not is_positive_number(servings):
            self._my_errors['servings'].append('Must be greater than zero.')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean
