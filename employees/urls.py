from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView
from .views import hr_register

urlpatterns = [
    
    path("register/", hr_register, name="hr_register"),
    
    path('login/', LoginView.as_view(template_name='employees/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    path('employees/', views.employee_list, name='employee_list'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employee/create/', views.employee_create, name='employee_create'),
    path('employee/update/<int:pk>/', views.employee_update, name='employee_update'),
    path('employee/delete/<int:pk>/', views.employee_delete, name='employee_delete'),

    path('visa/create/<int:employee_id>/', views.visa_create, name='visa_create'),
    path('visa/update/<int:pk>/', views.visa_update, name='visa_update'),
    path('visa/delete/<int:pk>/', views.visa_delete, name='visa_delete'),
    
    
    path('employee/<int:employee_id>/upload_document/', views.upload_employee_document, name='upload_employee_document'),
    path('employee/<int:employee_id>/delete_document/<int:document_id>/', views.delete_employee_document, name='delete_employee_document'),   
]






