
from django.db import models

class Student(models.Model):
    roll = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    mail = models.EmailField()
    pswd = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.roll


class Category(models.Model):
    cat_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cat_name


class Staff(models.Model):
    emp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    mail = models.EmailField()
    mobile = models.CharField(max_length=15)
    pswd= models.CharField(max_length=100, null=False)
    def __str__(self):
        return self.emp_id


class Complaint(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Solved", "Solved"),
    ]
    title = models.TextField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

# Create your models here.
