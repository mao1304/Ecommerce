from django.contrib import admin
from .models import Category, SubCategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('Category_name',)}
    list_display = ('Category_name', 'slug')

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('SubCategory_name',)}
    list_display = ('SubCategory_name', 'slug','Category_name')
