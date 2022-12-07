
from . import views

from django.urls import path

urlpatterns = [
    path('',views.index, name='index'),
    path('register/',views.register, name='register'),
    path('dashboard/',views.dashboard, name='dashboard' ),
    path('dashboard/add/',views.add, name='add' ),
    path('logout/',views.logout_request, name='logout' ),
    path('newuser/',views.newuser, name='newuser' ),
    path('dashboard/add_fine/',views.add_fine, name='add_fine' ),
    
    path('userfine_search',views.userfine_search, name='userfine_search' ),
    path('user_payment/<int:id>',views.user_payment, name='user_payment' ),
    
    path('dashboard/view_users/',views.view_users, name='view_users' ),
    path('dashboard/view_users/edit_road_user/<str:pk>',views.edit_road_user, name='edit_road_user' ),
    
    path('dashboard/add/create_onroadUser',views.create_onroadUser, name='create_onroadUser' ),
    path('dashboard/view_users/deleteRegUser/<int:id>/',views.delete_RegUser, name='deleteRegUser' ),
    path('dashboard/view_users/deleteRegUser/',views.delete_RegUser, name='deleteRegUser' ),
    path('dashboard/add_fine/getuser_details',views.getuser_details, name='getuser_details' ),
    
    path('dashboard/add_fine/penalty',views.penalty, name='penalty' ),
    path('dashboard/add_fine/view_challan/<int:id>',views.view_challan, name='view_challan' ),
   
    
    
]