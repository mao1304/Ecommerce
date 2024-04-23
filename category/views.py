from rest_framework import permissions, viewsets


from .serializer import CategorySerializer, SubCategorySerializer
from .models import Category, SubCategory


### clase para permitir solo el metodo GET
class readOnlyUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
            return request.method == 'GET'

class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [readOnlyUserPermission]
    queryset = Category.objects.all()
    # print('si esta entrando a la view')
    # def get_queryset(self):  
    #     categories = None
    #     category_slug = self.kwargs.get('category_slug')
    #     print(category_slug)
    #     if  category_slug == None:         
    #         categories = Category.objects.all()
                 
    #     return categories

class SubCategoryView(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    permission_classes = [readOnlyUserPermission]
    queryset = SubCategory.objects.all()

    # def get_queryset(self):  
    #     SubCategories = None
    #     Subcategory_slug = self.kwargs.get('Subcategory_slug')

    #     if  Subcategory_slug == None:         
    #         SubCategories = SubCategory.objects.all()
                 
    #     return SubCategories
    

