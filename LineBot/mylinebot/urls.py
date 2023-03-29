from django.contrib import admin
from django.urls import path, include
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('foodlinebot/', include('foodlinebot.urls')) #包含應用程式的網址
]