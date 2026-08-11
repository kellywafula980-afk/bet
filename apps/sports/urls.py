from django.urls import path
from . import views

app_name = 'sports'
urlpatterns = [
    path('', views.home, name='home'),
    path('sports/', views.sports_list, name='sports_list'),
    path('sport/<slug:sport_slug>/', views.leagues_list, name='leagues_list'),
    path('league/<slug:league_slug>/', views.matches_list, name='matches_list'),
    path('match/<int:match_id>/', views.match_detail, name='match_detail'),
]
