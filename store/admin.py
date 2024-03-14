from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('Product_name',)}
    list_display = ('Product_name','price', 'stock', 'Category','modified_date','is_available')
