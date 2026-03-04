from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('check-username/', views.CheckUsernameView.as_view(), name='check_username'),
    path('mypage/', views.MyPageView.as_view(), name='mypage'),
]
