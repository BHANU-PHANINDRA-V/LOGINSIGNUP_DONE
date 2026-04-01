from django.urls import path
from . import views

urlpatterns = [
    # --- HTML Pages ---
    path('', views.index_page, name='index'),
    path('login-page/', views.login_page, name='login_page'),
    path('signin-page/', views.signin_page, name='signin_page'),
    path('student/', views.student_page, name='student_page'),
    path('staff/', views.staff_page, name='staff_page'),
    path('complaint/', views.complaint_page, name='complaint_page'),
    path('complaint-success/', views.complaint_success, name='complaint_success'),
    path('change-password/', views.change_password_page, name='change_password_page'),

    # --- API Endpoints ---
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('update_password/', views.update_password, name='update_password'),
    path('student_profile/<str:roll>/', views.student_profile, name='student_profile'),
    path('staff_profile/<int:emp_id>/', views.staff_profile, name='staff_profile'),
    path('hostels/', views.hostel_list, name='hostel_list'),
    path('categories/', views.category_list, name='category_list'),
    
    path('register_complaint/', views.register_complaint, name='register_complaint'),
    path('search_complaint/<int:cid>/', views.search_complaint, name='search_complaint'),
    path('student_complaints/<str:roll>/<str:status>/', views.student_complaints, name='student_complaints'),
    path('staff_complaints/<int:emp_id>/', views.staff_complaints, name='staff_complaints'),
    path('complaint_details/<int:cid>/', views.complaint_details, name='complaint_details'),
    path('update_status/', views.update_status, name='update_status'),
    path('chief_warden_stats/<int:emp_id>/', views.chief_warden_monthly_stats, name='chief_warden_monthly_stats'),
    path('complaint_stats/', views.complaint_stats, name='complaint_stats'),
    
    # NEW: Endpoint for Staff to add workers
    path('add_worker/', views.add_worker, name='add_worker'),
]
