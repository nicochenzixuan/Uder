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
    path('welcome/start_ride', views.start_ride, name = 'start_ride'),
    path('welcome/ride_select', views.ride_select, name = 'ride_select'),
    path('welcome/ride_select/edit_request/<int:request_id>/', views.edit_request, name = 'edit_request'),
    #path('cancel_request/<int:request_id>', views.cancel_request, name = 'cancel_request')
    path('logout', views.user_logout, name = 'logout'),
    path('delete_driver/', views.delete_driver, name = 'delete_driver'),
    path('welcome/share_search/', views.share_search, name = 'share_search'),
    path('welcome/driver_search/', views.driver_search, name = 'driver_search'),
    path('join_ride/<int:request_id>/', views.join_ride, name = 'join_ride'),
    path('confirm_request/<int:request_id>/', views.confirm_request, name = 'confirm_request'),
    
    
    ###
    path('complete_ride/<int:request_id>/', views.complete_ride, name = 'complete_ride'),
    
    
 
    #path('find_confirmed_rides/', views.find_confirmed_rides, name = 'find_confirmed_rides'),
    
    #path('welcome/confirmed_display/', views.confirmed_display, name = 'confirmed_display'),
    #path('welcome/share_search_display/', views.share_search_display, name = 'share_search_display'),
    
    #new
    path('welcome/confirmed_display', views.confirmed_display, name = 'confirmed_display'),
    

]

