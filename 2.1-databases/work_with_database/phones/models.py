from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=1, validators=[MinValueValidator(0)])
    image = models.URLField(max_length=500, blank=True)
    release_date = models.DateField(null=True, blank=True)
    lte_exists = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name