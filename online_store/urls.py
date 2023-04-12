from django.contrib import admin
from django.urls import path
from django.urls import include, path
from my_store_app.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("my_store_app.urls")),
]
