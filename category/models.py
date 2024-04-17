from django.db import models
from django.urls import reverse

class Category(models.Model):
    Category_name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=100, unique=True)
    cat_image = models.CharField( max_length=50)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
    
    def __str__(self):
        return self.Category_name
    
class SubCategory(models.Model):
    Category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    SubCategory_name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=100, unique=True)
    cat_image = models.CharField( max_length=250)
    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'

    def get_url(self):
        return reverse('products_by_Subcategory', args=[self.slug])
    
    def __str__(self):
        return self.SubCategory_name
