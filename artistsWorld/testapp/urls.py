from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('image', views.show_image, name='image'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('publish', views.publish, name='publish'),
    path('edit_publish', views.edit_publish, name='edit_publish'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile')
]
