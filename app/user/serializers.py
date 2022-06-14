
from wsgiref.validate import validator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from user.validators import password_complex_validator
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """ 🪢 (❁´◡`❁)  serializer for users object  (❁´◡`❁) 🪢 """

    class Meta:
        model =  User
        fields = ['name','email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'validators':[password_complex_validator,]}}
        
    def create(self, validated_data):
        """ φ(゜▽゜*)♪   creating user with encrypted password φ(゜▽゜*)♪ """

        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """✍️(◔◡◔) updating user if password update then encrypting it first ┬┴┬┴┤(･_├┬┴┬┴"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user
    
    