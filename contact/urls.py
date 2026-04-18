from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_form, name='contact'),
    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/<int:pk>/toggle/', views.message_toggle_read, name='message_toggle_read'),
    path('messages/<int:pk>/delete/', views.message_delete, name='message_delete'),
]
