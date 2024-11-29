from django.urls import path
from . import views

urlpatterns = [
    # GET Endpoints
    path('Users/', views.get_users, name='get_users'),
    path('Uses/', views.get_uses, name='get_uses'),
    path('Payment/', views.get_payment, name='get_payment'),
    path('DryerHistory/', views.get_dryer_history, name='get_dryer_history'),
    path('LaundryDevice/', views.get_laundry_device, name='get_laundry_device'),

    # POST Endpoints
    path('Payment/create/', views.make_payment, name='create_payment'),
    path('Uses/create/', views.create_use, name='create_uses'),
    path('LaundryDevice/create/', views.create_laundry_device, name='create_laundry_device'),
    path('Users/create/', views.create_user, name='create_user'),
    path('DryerHistory/create/', views.create_dryer_history, name='create_dryer_history'),

    # PUT Endpoints
    path('Payment/<int:payment_id>/update/', views.update_payment, name='update_payment'),
    path('Uses/update/', views.update_uses, name='update_uses'),
    path('LaundryDevice/<int:machine_id>/update/', views.update_laundry_device, name='update_laundry_device'),
    path('Users/<str:username>/update/', views.update_user, name='update_user'),
    path('DryerHistory/<int:dryer_id>/update/', views.update_dryer_history, name='update_dryer_history'),

    # DELETE Endpoints
    path('Payment/<int:payment_id>/delete/', views.delete_payment, name='delete_payment'),
    path('Uses/delete/', views.delete_uses, name='delete_uses'),
    path('LaundryDevice/<int:machine_id>/delete/', views.delete_laundry_device, name='delete_laundry_device'),
    path('Users/<str:username>/delete/', views.delete_user, name='delete_user'),
    path('DryerHistory/<int:dryer_id>/delete/', views.delete_dryer_history, name='delete_dryer_history'),
]
