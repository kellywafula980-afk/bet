from django.urls import path
from . import views

app_name = 'payments'
urlpatterns = [
    path('deposit/', views.deposit, name='deposit'),
    path('verify/', views.verify, name='verify'),
    path('withdraw/', views.withdraw, name='withdraw'),
]
