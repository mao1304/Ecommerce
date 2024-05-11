from django.db import models
from django.urls import reverse

class Category(models.Model):
    Category_name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=100, unique=True)
    Type = models.CharField(max_length=50)
    cat_image = models.CharField( max_length=255)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
    
    def __str__(self):
        return self.Category_name
    

