from django.urls import path
from doorlock import views


urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('index/', views.index, name='index'),
    path('sc252/', views.unlock_door_SC252, name='unlock_door_SC252'),
    path('sc251/', views.unlock_door_SC251, name='unlock_door_SC251'),
    path('sc250/', views.unlock_door_SC250, name='unlock_door_SC250'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('add_user/', views.add_user, name='add_user'),
]