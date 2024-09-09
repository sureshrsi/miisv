from django.urls import path
from .views import signup, profile, add_address

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('profile/add-address/', add_address, name='add_address'),
]
