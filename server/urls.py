from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Complex Django administration'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/bookstore/', include('bookstore.urls'))
]
