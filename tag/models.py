from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # Dynamic model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # ID from dynamic model
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey('content_type', 'object_id')

    def get_slug(self):
        slug = slugify(self.name)
        unique_slug = slug

        number = 1
        while Tag.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{number}'
            number += 1

        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
