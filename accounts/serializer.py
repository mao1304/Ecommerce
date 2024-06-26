from rest_framework import serializers

from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name','last_name', 'email', 'password']

    # def create(self, validated_data):
    #     username = validated_data['email'].split('@')[0]
    #     user = Account.objects.create_user(username=username, **validated_data)
    #     return user





# class RegistrationSerializer(serializers.Serializer):
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     email = serializers.EmailField()
#     password = serializers.CharField()

#     def create(self, validated_data):
#         username = validated_data['email'].split('@')[0]
#         user = Account.objects.create_user(username=username, **validated_data)
#         return user
    
# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()