from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from . import views
urlpatterns = [
    path("signup/", views.SignUpView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("user/", views.UserView.as_view({"post": "create", "get": "list"})),
    path("user/<uuid:pk>",
         views.UserView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),

]
