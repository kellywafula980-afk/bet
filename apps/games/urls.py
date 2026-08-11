from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'games'
urlpatterns = [
    path('', RedirectView.as_view(url='/games/wheel/', permanent=False), name='home'),
    path('wheel/', views.wheel_page, name='wheel'),
    path('spin/', views.spin_api, name='spin_api'),
    path('toggle-demo/', views.toggle_demo, name='toggle_demo'),
]
