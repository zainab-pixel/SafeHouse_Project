from django.contrib import admin
from django.urls import path
from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/set_state/', views.set_state, name='set_state'),
]
