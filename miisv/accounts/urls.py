from django.urls import path
from .views import signup, signin, signout, profile, add_address

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('profile/', profile, name='profile'),
    path('profile/add-address/', add_address, name='add_address'),
]
