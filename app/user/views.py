
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import get_user_model


from user.serializers import UserSerializer

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
