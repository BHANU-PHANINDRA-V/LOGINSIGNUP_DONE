from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup),
 path("login/", views.login),
  path("register_complaint/", views.register_complaint),
    path("search_complaint/<int:cid>/", views.search_complaint),
    path("staff_complaints/<str:emp_id>/", views.staff_complaints),
    path("update_status/", views.update_status),
     path("complaint_stats/", views.complaint_stats),
      path("staff_signup/", views.staff_signup),
      path("staff_login/", views.staff_login),
       path("student_complaints/<int:roll>/<str:status>/", views.student_complaints)
]
#path 1st argument is api endpoint, 2nd argument is the view function that will handle the request to that endpoint