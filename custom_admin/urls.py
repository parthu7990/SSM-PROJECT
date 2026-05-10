from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    
    # Inquiries
    path('inquiries/', views.inquiries_list, name='inquiries_list'),
    path('inquiries/<int:pk>/', views.inquiry_detail, name='inquiry_detail'),
    
    # Services
    path('services/', views.services_list, name='services_list'),
    path('services/create/', views.service_create, name='service_create'),
    path('services/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
    
    # Clients
    path('clients/', views.clients_list, name='clients_list'),
    path('clients/create/', views.client_create, name='client_create'),
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
    
    # Company Info
    path('company-info/', views.company_info, name='company_info'),
    
    # Newsletter
    path('newsletter/', views.newsletter_subscribers, name='newsletter_subscribers'),
]
