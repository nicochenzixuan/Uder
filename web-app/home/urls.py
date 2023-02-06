from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('welcome/', views.welcome, name = 'welcome'),  
    #path('<str:username>/welcome/', views.welcome, name = 'welcome'),
    path('welcome/driver', views.driver, name = 'driver'),
    #path('<int:question_id>/vote/', views.vote, name='vote'),
    
    path('welcome/profile/', views.update_driver_info, name = 'profile'),
    path('welcome/user_profile/', views.update_user_info, name = 'user_profile'),
    
    path('welcome/ride_request', views.ride_request, name = 'ride_request'),
    path('logout', views.user_logout, name = 'logout'),
    path('driverCancel/', views.driverCancel, name = 'driverCancel'),
]

