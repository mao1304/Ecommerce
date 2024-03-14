from django.shortcuts import get_object_or_404
from rest_framework import  viewsets

from .serializer import ProductSerializer
from .models import Product
from category.views import readOnlyUserPermission
from category.models import Category


## view para retornar todas las categorias solo metodo "GET"
class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [readOnlyUserPermission]
    queryset = Product.objects.all()
    print("primer passo ")

    def get_queryset(self):  
        print("2 passo ")
        Products = None
        categories = None 
        category_slug = self.kwargs.get('category_slug')
        print(Products)

        if  category_slug == 'products':         
            print(f"entro fue aqui {Products}") 
            Products = Product.objects.all().filter(is_available=True)
        
        elif category_slug != None:
             print(f"entro aqui {Products}")
             categories = get_object_or_404(Category, slug=category_slug)
             Products = Product.objects.filter(Category=categories, is_available=True) 

            
        return Products
