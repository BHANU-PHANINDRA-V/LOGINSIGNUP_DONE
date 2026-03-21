from django.urls import path
from . import views

urlpatterns = [
    # --- HTML Pages (What you see in the browser) ---
    path('', views.index_page, name='index'),
    path('login-page/', views.login_page, name='login_page'),
    path('signin-page/', views.signin_page, name='signin_page'),
    path('student/', views.student_page, name='student_page'),
    path('staff/', views.staff_page, name='staff_page'),
    path('complaint/', views.complaint_page, name='complaint_page'),

    # --- API Endpoints (What your JavaScript fetch() calls in the background) ---
    path('signup/', views.signup, name='signup'),
    path('staff_signup/', views.staff_signup, name='staff_signup'),
    path('login/', views.login, name='login'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('register_complaint/', views.register_complaint, name='register_complaint'),
    path('search_complaint/<int:cid>/', views.search_complaint, name='search_complaint'),
    path('student_complaints/<int:roll>/<str:status>/', views.student_complaints, name='student_complaints'),
    path('staff_complaints/<str:emp_id>/', views.staff_complaints, name='staff_complaints'),
    path('update_status/', views.update_status, name='update_status'),
    path('complaint_stats/', views.complaint_stats, name='complaint_stats'),
]