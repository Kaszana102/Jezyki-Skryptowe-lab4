from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('image', views.image, name='image'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('publish', views.publish, name='publish'),
    path('logout', views.logout, name='logout')
]
