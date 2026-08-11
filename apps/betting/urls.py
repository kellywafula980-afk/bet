from django.urls import path
from . import views

app_name = 'betting'
urlpatterns = [
    path('place/', views.place_bet, name='place_bet'),
    path('my-bets/', views.my_bets, name='my_bets'),
]
