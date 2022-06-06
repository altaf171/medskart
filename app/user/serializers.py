
from wsgiref.validate import validator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from user.validators import password_complex_validator
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """ 🪢 (❁´◡`❁)  serializer for users object  (❁´◡`❁) 🪢 """

    # password = serializers.CharField(
    #     source = 'user',
    #     write_only=True,
    #     required=True,
    #     help_text='Leave empty if no change needed',
    #     style={'input_type': 'password', 'placeholder': 'Password'},
    #     validators = [password_complex_validator,]

    # )

    class Meta:
        model =  User
        fields = ['name','email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'validators':[password_complex_validator,]}}
        
    def create(self, validated_data):
        """ φ(゜▽゜*)♪   creating user with encrypted password φ(゜▽゜*)♪ """

        return User.objects.create_user(**validated_data)

    
    