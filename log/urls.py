from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from log.views import IndexView


app_name = 'log'

urlpatterns = [
    path('', IndexView, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
