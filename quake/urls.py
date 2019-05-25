from django.contrib import admin
from django.urls import path, include
from log import urls as log_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(log_urls)),
]
