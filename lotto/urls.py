from django.urls import path
from . import views

app_name = 'lotto' 

urlpatterns = [
    
    path('', views.index, name='index'),
    path('buy/', views.buy_ticket, name='buy_ticket'),
    path('draw/', views.admin_draw, name='admin_draw'),
    path('accounts/signup/', views.signup, name='signup'),
]
