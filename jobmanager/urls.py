from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.adminlogout, name='loggedout'),

    path('success/', views.success, name='success'),
    path('success/profile/', views.profile, name='profile'),
    path('success/applycompany/<str:company>', views.applycompany, name='applycompany'),

    path('superuser/', views.superuser, name='superuser'),
    path('superuser/appliedstudents/', views.appliedstudents, name='appliedstudents'),
    path('superuser/companies/', views.allcompanies, name='allcompany'),
    path('superuser/selectedstudents/', views.selectedstudents, name='selectedstudents'),
    path('superuser/students/', views.allstudents, name='allstudents'),

    path('superuser/deletecompanies/', views.deleteallCompanies, name='deletecompanies'),
    path('superuser/deletestudents/', views.deleteallStudents, name='deletestudents'),

    path('company/', views.company, name='company'),
    path('company/selectstudent/', views.selectstudent, name='selectstudent'),
]
