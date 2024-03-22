
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets


from .serializer import CategorySerializer
from .models import Category


### clase para permitir solo el metodo GET
class readOnlyUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
            return request.method == 'GET'
    

class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [readOnlyUserPermission]
    queryset = Category.objects.all()

    def get_queryset(self):  
        categories = None
        category_slug = self.kwargs.get('category_slug')
        print(categories)

        if  category_slug == 'all':         
            categories = Category.objects.all()
                 
        return categories

         
    

