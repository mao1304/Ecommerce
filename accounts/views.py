from django.shortcuts import render
from django.core.exceptions import SuspiciousOperation
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,logout,login 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .forms import RegistrationForm
from .models import Account
# from .serializer import LoginSerializer

@api_view(['POST'])
def registrer(request):
    return Response({registrer})

# class registrer(APIView):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def post(self, request):
#         serializer = RegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Registro exitoso'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@method_decorator(csrf_exempt, name='dispatch')
class Login(APIView):
    print('entro al login view')
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        print(f"entro aqui y este es el serializer{serializer}")
        if serializer.is_valid():
            try:
                print('era valido el forms')
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                print(f'datos del form{email}{password}')

                user = authenticate(request, email=email,password=password)
                print(user)
                if user is None: 
                    raise SuspiciousOperation("Credenciales incorrectas")
                
                login(request, user)
                return Response({'message':'Inicio de sesión exitoso'},status=status.HTTP_200_OK)
            
            except SuspiciousOperation as e:
                return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)



@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class logout(APIView):
 def post(self, request):
        request.session.flush()
        logout(request)
        return Response({'message': 'Cierre de sesión exitoso'}, status=status.HTTP_200_OK)