
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views


urlpatterns = [
  
    path('about_me/', views.about_me),
    path('',views.landing),
    path('login/', views.loginview, name='loginview'),
    path('loginprocess/', views.loginprocess, name='loginprocess'),
    path('signup/', views.signup, name='signup'),
    path('', views.landing, name='home'),
    path('logout/', views.logout, name='logout'),
    path('save_point/', views.save_point, name='savepoint'),
    path('view_point/', views.view_point, name='viewpoint'),
]