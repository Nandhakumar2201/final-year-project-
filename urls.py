from django.urls import path

from .views import login_view, register_view 

urlpatterns = [
    path("api/register/", register_view),
    path('login/', login_view, name='login'),
]
