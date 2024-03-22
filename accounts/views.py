from django.shortcuts import render
from django.core.exceptions import SuspiciousOperation
from django.db import IntegrityError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import RegistrationForm
from .models import Account


class registrer(APIView):
    def post(self, request):
        form = RegistrationForm(request.data)   
        if form.is_valid():
            try:
                first_name= form.cleaned_data['first_name']
                last_name= form.cleaned_data['last_name']
                email= form.cleaned_data['email']
                password= form.cleaned_data['password']
                username = email.split('@')[0]
                
                user = Account.objects.create_user(first_name=first_name,
                                                   last_name= last_name,
                                                   username=username, email=email,
                                                   password=password)
                user.save()

                response = Response({'message': 'Registro exitoso'}, status=status.HTTP_201_CREATED)
                return response
            
            except IntegrityError as e:
                return Response({'error':'datos no validos'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            print('formulario no valido')
            return Response({'error':'formulario no valido'}, status=status.HTTP_400_BAD_REQUEST)



                # request.session.flush()
                # logout(request)
                # raise ValueError

# class login(APIView):
#     pass

# class logout(APIView):
#     pass
