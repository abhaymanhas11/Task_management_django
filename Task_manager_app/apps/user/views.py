from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apps.todo import urls
from django.shortcuts import redirect
from django.views import View
from apps.user.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.user.serializer import RegisterSerializer, LoginSerializer
from apps.user.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from apps.utils.enum import UserType
from rest_framework.permissions import IsAdminUser


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = ()


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
            if obj.user_type==UserType.admin.value:
                obj.is_staff=True
                obj.is_superuser=True
            elif obj.user_type==UserType.editor.value:
                obj.is_staff=True
            obj.is_active = True
            obj.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(status=status.HTTP_404_NOT_FOUND)


# login user
class LoginUser(View):
    def get(self, request):
        return render(request, "user/login.html")

    @csrf_exempt
    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("/todo/dashboard")

        else:
            messages.error(request, " Please enter the correct details")
            return redirect("/")


@login_required
def Userlogout(request):
    logout(request)
    return redirect("/")
