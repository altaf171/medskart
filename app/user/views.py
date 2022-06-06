from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model


from user.serializers import UserSerializer

User = get_user_model()

class UserCreateAPIView(CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializer

