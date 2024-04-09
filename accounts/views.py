from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,logout,login 
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import  IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

from .models import Account
from .serializer import AccountSerializer
from Cart.views import _cart_id
from Cart.models import Cart, CartItem


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  

@api_view(['POST'])
def registrer(request):
    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        user = Account.objects.get(email=serializer.data['email'])
        user.set_password(serializer.data['password'])
        user.save()
        token = Token.objects.create(user=user)

        return Response({'token': token.key, 'user': serializer.data }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@method_decorator(login_required, name='dispatch')
class profile(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer = AccountSerializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Logout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.session.flush()
        logout(request)
        return Response({'message': 'session successfully closed '}, status=status.HTTP_200_OK)




@method_decorator(csrf_exempt, name='dispatch')
class Login(APIView):
    # authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart = Cart.objects.get(Cart_id=_cart_id(request))
            is_cart_item_exists = CartItem.objects.filter(Cart=cart).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.filter(Cart=cart, is_active=True)
                for item in cart_item:
                    item.user = user
                    item.save()
        except:
            pass

        login(request, user)  
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key, 'createtoken': created, 'user': AccountSerializer(user).data}, status=status.HTTP_200_OK)

