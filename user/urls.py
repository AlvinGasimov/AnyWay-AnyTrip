from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('submitemail/', submitemail, name='submitemail'),
    path('account/', account, name='account'),
]