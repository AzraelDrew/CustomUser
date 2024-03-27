from django.contrib.auth import authenticate
from django.utils.timezone import now
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .serializers import SignUpSerializer, UserSerializer
from .models import User
from .tokens import create_jwt_pair_for_user

# Create your views here.


class SignUpView(APIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            user.last_login = now()
            user.save(update_fields=["last_login"])
            token = create_jwt_pair_for_user(user)
            return Response(data=token, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid email or password"})


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
