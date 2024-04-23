from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from rest_framework import  viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializer import ProductSerializer
from .models import Product
from category.views import readOnlyUserPermission
from category.models import Category, SubCategory
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
@method_decorator(csrf_exempt, name='dispatch')
class product_detail(APIView):
    def get(self, request):
    #     return Response({'message': 'hello word!'},status=status.HTTP_200_OK)
    # # print("1")
    # # def post(self, request):
        product_slug = request.data.get('product_slug')

        try: 
            single_product = Product.objects.get( slug=product_slug)
            in_cart = CartItem.objects.filter(Cart__Cart_id=_cart_id(request), Product=single_product).exists()
        except Product.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        Product_serializer = model_to_dict(single_product) 
        context = {
            'single_product': Product_serializer,
            'in_cart': in_cart,
        }
        return Response(context, status=status.HTTP_200_OK)