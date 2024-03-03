from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('sc252/', views.unlock_door_SC252, name='unlock_door_SC252'),
    path('sc251/', views.unlock_door_SC251, name='unlock_door_SC251'),
    path('sc250/', views.unlock_door_SC250, name='unlock_door_SC250'),
    path('index/', views.index, name='index'),
    path('importuser/', views.add_user, name='importuser'),
]