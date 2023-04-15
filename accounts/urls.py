from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.UserView.as_view()),
    path('token/create/', views.CreateTokenView.as_view()),
    path('token/refresh/', views.TokenRefreshView.as_view()),
]
