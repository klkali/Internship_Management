from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import CustomLoginView, register, student_dashboard, company_dashboard
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='main/login.html'), name='home'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', CustomLoginView.as_view(template_name='main/logout.html'), name='logout'),
    path('company-dashboard/', views.company_dashboard, name='company_dashboard'),
    path('create-internship/', views.create_internship, name='create_internship'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('internship/<int:pk>/', views.internship_details, name='internship_details'),
    path('internship/<int:pk>/apply/', views.apply_for_internship, name='apply_for_internship'),
    path('company-profile/', views.company_profile, name='company_profile'),
    path('edit-internship/<int:pk>/', views.edit_internship, name='edit_internship'),
    path('delete-internship/<int:pk>/', views.delete_internship, name='delete_internship'),
    path('student-profile/', views.student_profile, name='student_profile'),
    path('manage-applications/', views.manage_applications, name='manage_applications'),
    path('update-application-status/<int:pk>/<str:status>/', views.update_application_status, name='update_application_status'),
    path('available-internships/', views.available_internships, name='available_internships'),
]
