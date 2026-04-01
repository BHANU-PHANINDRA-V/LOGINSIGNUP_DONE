from django.db import models


# -------------------- HOSTEL --------------------
class Hostel(models.Model):
    hostel_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        # ❌ WRONG: return self.hostel_id (integer)
        # ✅ Django expects string in __str__
        return str(self.name)   # ✔️ better readable than ID


# -------------------- STATUS --------------------
class Status(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Solved", "Solved"),
    ]

    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        # ❌ WRONG: return self.status_id
        # ✅ should return meaningful string
        return self.status_name


# -------------------- STUDENT --------------------
class Student(models.Model):
    # ❌ WRONG: IntegerField for roll
    # ✅ roll numbers may contain letters or leading zeros
    roll = models.CharField(max_length=20, primary_key=True)

    name = models.CharField(max_length=100)
    mail = models.EmailField()

    # ❌ WRONG: max_length=100 + plain password
    # ✅ hashed passwords need more space
    pswd = models.CharField(max_length=128)

    mobile = models.CharField(max_length=15)

    hostel_id = models.ForeignKey(Hostel, on_delete=models.CASCADE)

    def __str__(self):
        # ❌ WRONG: return self.roll (if int earlier)
        return str(self.roll)


# -------------------- CATEGORY --------------------
class Category(models.Model):
    cat_id = models.IntegerField(primary_key=True)
    cat_name = models.CharField(max_length=100)

    def __str__(self):
        # ❌ WRONG: returning ID
        return self.cat_name


# -------------------- DESIGNATION --------------------
class Designation(models.Model):
    DESIGNATION_CHOICES = [
        ("Chief Warden", "Chief Warden"),
        ("Warden", "Warden"),
        ("Care Taker", "Care Taker"),
    ]

    desig_id = models.AutoField(primary_key=True)
    desig_name = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)

    def __str__(self):
        # ❌ WRONG: return self.desig_id
        return self.desig_name


# -------------------- STAFF STATUS --------------------
class StaffStatus(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]

    staff_status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")

    def __str__(self):
        return self.status_name


# -------------------- STAFF --------------------
class Staff(models.Model):
    emp_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    mail = models.EmailField()
    mobile = models.CharField(max_length=15)

    # ❌ WRONG:
    # 1. No default temp password
    # 2. Not enough length for hashed password
    pswd = models.CharField(max_length=128, default="Collage@123")

    # ✅ Needed for first login password change system
    #first_login = models.BooleanField(default=True)

    desig_id = models.ForeignKey(Designation, on_delete=models.CASCADE)
    first_login = models.BooleanField(default=True)
    # ❌ WRONG:
    # 1. Field name "Hostel_id" (bad naming convention)
    # 2. Chief Warden may not belong to hostel → must allow NULL
    hostel_id = models.ForeignKey(Hostel, on_delete=models.CASCADE, null=True, blank=True)

    staff_status_id = models.ForeignKey(StaffStatus, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.emp_id)


# -------------------- COMPLAINT --------------------
class Complaint(models.Model):
    # ❌ WRONG: IntegerField primary key (manual handling)
    # ✅ use AutoField
    Complaint_id = models.AutoField(primary_key=True)

    title = models.TextField()
    description = models.TextField()
    attachment = models.FileField(upload_to='complaint_images/', null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)

    # ❌ WRONG: required field → error during complaint creation
    # ✅ should be optional
    solved_date = models.DateTimeField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    hostel_id = models.ForeignKey(Hostel, on_delete=models.CASCADE)

    # ❌ WRONG: should allow NULL (not assigned initially)
    solved_by = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


# -------------------- TECHNICAL WORKER --------------------
class TechnicalWorker(models.Model):
    # ❌ WRONG: class name Technical_worker (not python standard)
    worker_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        # ❌ WRONG: returning int
        return str(self.name)
