from django.urls import path
from . import views
from .views import signup


urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('profile/', views.profile, name='profile'), 
    path('signup/', signup, name='signup'),
    path('reviews/<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('reviews/<int:pk>/delete/', views.delete_review, name='delete_review'),

]
