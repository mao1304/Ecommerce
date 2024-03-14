
from rest_framework import permissions, viewsets


from .serializer import CategorySerializer
from .models import Category


### clase para permitir solo el metodo GET
class readOnlyUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
            return request.method == 'GET'
    

## view para retornar todas las categorias solo metodo "GET"
class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [readOnlyUserPermission]


    def get_queryset(self):   

        category_slug = self.kwargs.get('category_slug')
        queryset = Category.objects.all() 

        if category_slug == 'categories':
            return queryset

        else:
             queryset = queryset.filter(slug=category_slug)
            
        return queryset
            
         
    

