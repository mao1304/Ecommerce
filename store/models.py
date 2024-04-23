from django.db import models
from django.urls import reverse


from category.models import SubCategory, Category

class Product(models.Model):
    Product_name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    brand = models.CharField(max_length=100)
    images = models.CharField( max_length=250)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    SubCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True)
    created_date = models.DateTimeField( auto_now_add=True)
    modified_date = models.DateTimeField( auto_now=True)

    def formatted_price(self):
        return '{:,.0f}'.format(self.price) 

    def get_url(self):
        return reverse('product_detail', args=[self.SubCategory.slug, self.slug])

    def __str__(self):
        return self.Product_name
