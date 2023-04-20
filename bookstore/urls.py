from django.urls import path

from bookstore import views

urlpatterns = [
    path('booklist/', views.BookListAPIView.as_view()),
    path('storelist/', views.StoreListAPIView.as_view())
]
