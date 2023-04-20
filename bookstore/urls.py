from django.urls import path

from bookstore import views

urlpatterns = [
    path('booklist/', views.SelectBookListAPIView.as_view())
]
