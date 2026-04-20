from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authors.urls')),
    path('api/', include('quizes.urls')),
    path('api/', include('yasg.urls')),
]
