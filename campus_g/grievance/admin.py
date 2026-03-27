

# Register your models here.
from django.contrib import admin
from .models import Student, Category, Staff, Complaint, Hostel, Status, Designation, StaffStatus, TechnicalWorker

admin.site.register(Student)
admin.site.register(Category)
admin.site.register(Staff)
admin.site.register(Complaint)
admin.site.register(Hostel)
admin.site.register(Status)
admin.site.register(Designation)
admin.site.register(StaffStatus)
admin.site.register(TechnicalWorker)