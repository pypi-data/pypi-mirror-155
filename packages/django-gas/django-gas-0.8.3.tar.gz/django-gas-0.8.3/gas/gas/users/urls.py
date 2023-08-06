from django.urls import path

from . import views


urlpatterns = [
    path('', views.UserList.as_view(), name="user_list"),
    path('create/', views.CreateUser.as_view(), name="user_create"),
    path('<int:pk>/edit/', views.UpdateUser.as_view(), name="user_update"),
    path('<int:pk>/change-password/', views.ChangePasswordUser.as_view(), name="user_change_password"),
    path('<int:pk>/delete/', views.DeleteUser.as_view(), name="user_delete"),
]
