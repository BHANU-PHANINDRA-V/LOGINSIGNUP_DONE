from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Category, Staff, Complaint

admin.site.register(Student)
admin.site.register(Category)
admin.site.register(Staff)
admin.site.register(Complaint)
