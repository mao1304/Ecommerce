from django.db import models
from django.urls import reverse


from category.models import Category

class Product(models.Model):
    Product_name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='images/Products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField( auto_now_add=True)
    modified_date = models.DateTimeField( auto_now=True)

    
    def get_url(self):
        return reverse('product_detail', args=[self.Category.slug, self.slug])

    def __str__(self):
        return self.Product_name
