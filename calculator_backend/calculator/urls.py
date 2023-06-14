from django.urls import path
from . import views
from .views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('operations/', views.operation_list, name='operations'),
    path('calculate/', views.calculate, name='calculate'),
    path('user-records/', views.list_user_records, name='list_user_records'),  
    path('users/', views.user_list, name='list_user'), 
    path('users/<int:user_id>/status/', views.user_status_view, name='user_status'),
]
