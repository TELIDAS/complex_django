from django.urls import path

from bookstore import views

urlpatterns = [
    path('publisher-list/', views.PublisherListAPIView.as_view()),
    path('book-list/', views.BookListAPIView.as_view()),
    path('store-list/', views.StoreListAPIView.as_view())
]
