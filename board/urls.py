from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.BoardListView.as_view(), name='list'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail'),
]
