from django.contrib.auth.views import logout_then_login
from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.GASLoginView.as_view(), name='login'),
    path('logout/', logout_then_login, {'login_url': 'gas:login'}, name='logout'),
    path('change-password/', views.GASPasswordChangeView.as_view(), name='change_password'),
    path('', views.Index.as_view(), name='index'),
]
