from django.shortcuts import get_object_or_404
from rest_framework import  viewsets

from .serializer import ProductSerializer
from .models import Product
from category.views import readOnlyUserPermission
from category.models import Category
from Cart.models import CartItem
from Cart.views import _cart_id

## view para retornar todas las categorias solo metodo "GET"
class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [readOnlyUserPermission]
    queryset = Product.objects.all()

    def get_queryset(self):  
        Products = None
        categories = None 
        category_slug = self.kwargs.get('category_slug')

        if  category_slug == 'products':         
            Products = Product.objects.all().filter(is_available=True)
        
        elif category_slug != None:
             categories = get_object_or_404(Category, slug=category_slug)
             Products = Product.objects.filter(Category=categories, is_available=True) 

            
        return Products

def product_detail(request, category_slug, product_slug):
    
    try: 
        single_product = Product.objects.get(Category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product = single_product).exists()
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request,'store/product_detail.html', context)