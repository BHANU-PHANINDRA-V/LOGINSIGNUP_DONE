from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json

from .models import (
    Student, Staff, Complaint, Category, 
    Hostel, Status, Designation, StaffStatus, TechnicalWorker
)

# --- REGISTRATION & LOGIN APIS ---
@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            hostel_obj = Hostel.objects.get(hostel_id=data["hostel_id"])
            Student.objects.create(
                roll=data["roll"],
                name=data["name"],
                mail=data["mail"],
                pswd=data["pswd"],
                mobile=data["mobile"],
                hostel_id=hostel_obj
            )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        exists = Student.objects.filter(roll=data["roll"], pswd=data["pswd"]).exists()
        return JsonResponse({"success": exists})

@csrf_exempt
def staff_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            # 1. Try to find the staff member
            staff = Staff.objects.get(emp_id=data["emp_id"], pswd=data["pswd"])
            
            # 2. Safely check Active Status
            try:
                if staff.staff_status_id.status_name != "Active":
                    return JsonResponse({"success": False, "error": "Your account has been disabled by the Admin."})
            except AttributeError:
                # If they don't have a status assigned, we let them pass rather than crashing
                pass

            # 3. Safely check First Login
            is_first_time = getattr(staff, 'first_login', False)
            if is_first_time:
                return JsonResponse({"success": True, "first_login": True})

            return JsonResponse({"success": True, "first_login": False})
            
        except Staff.DoesNotExist:
            return JsonResponse({"success": False, "error": "Invalid Staff Credentials"})
        except Exception as e:
            # 4. CRITICAL: Catch any other database errors and send them to the screen!
            return JsonResponse({"success": False, "error": f"Database Config Error: {str(e)}"})
@csrf_exempt
def update_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            new_password = data.get("new_pswd")
            current_password = data.get("current_pswd")

            if not new_password:
                return JsonResponse({"success": False, "error": "New password is required."})

            if data.get("emp_id") is not None:
                staff = Staff.objects.get(emp_id=data["emp_id"])

                if current_password and staff.pswd != current_password:
                    return JsonResponse({"success": False, "error": "Current password is incorrect."})

                staff.pswd = new_password
                staff.first_login = False
                staff.save()
                return JsonResponse({"success": True})

            if data.get("roll"):
                student = Student.objects.get(roll=data["roll"])

                if current_password and student.pswd != current_password:
                    return JsonResponse({"success": False, "error": "Current password is incorrect."})

                student.pswd = new_password
                student.save()
                return JsonResponse({"success": True})

            return JsonResponse({"success": False, "error": "User identifier is required."})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)

@csrf_exempt
def student_profile(request, roll):
    try:
        student = Student.objects.select_related("hostel_id").get(roll=roll)
        data = {
            "success": True,
            "role": "Student",
            "roll": student.roll,
            "name": student.name,
            "mail": student.mail,
            "mobile": student.mobile,
            "hostel": student.hostel_id.name if student.hostel_id else "Not Assigned",
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@csrf_exempt
def staff_profile(request, emp_id):
    try:
        staff = Staff.objects.select_related("desig_id", "hostel_id", "staff_status_id").get(emp_id=emp_id)
        data = {
            "success": True,
            "role": "Staff",
            "emp_id": staff.emp_id,
            "name": staff.name,
            "mail": staff.mail,
            "mobile": staff.mobile,
            "designation": staff.desig_id.desig_name if staff.desig_id else "Not Assigned",
            "hostel": staff.hostel_id.name if staff.hostel_id else "All Hostels",
            "staff_status": staff.staff_status_id.status_name if staff.staff_status_id else "Unknown",
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@csrf_exempt
def hostel_list(request):
    try:
        hostels = Hostel.objects.all().order_by("hostel_id")
        data = [{"hostel_id": hostel.hostel_id, "name": hostel.name} for hostel in hostels]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@csrf_exempt
def category_list(request):
    try:
        categories = Category.objects.all().order_by("cat_name")
        data = [{"cat_id": category.cat_id, "cat_name": category.cat_name} for category in categories]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


# --- COMPLAINT APIS ---
@csrf_exempt
@require_http_methods(["POST"])
def register_complaint(request):
    try:
        if request.content_type and "application/json" in request.content_type:
            data = json.loads(request.body)
            photo = None
        else:
            data = request.POST
            photo = request.FILES.get("photo")

        student = Student.objects.get(roll=data["roll"])
        category, _ = Category.objects.get_or_create(cat_name=data["category"])
        hostel_obj = Hostel.objects.get(hostel_id=data["hostel_id"])
        pending_status, _ = Status.objects.get_or_create(status_name="Pending")

        complaint = Complaint.objects.create(
            title=data["title"],
            description=data["description"],
            cat_id=category,
            student_id=student,
            hostel_id=hostel_obj,
            status_id=pending_status,
            attachment=photo
        )
        return JsonResponse({"success": True, "complaint_id": complaint.Complaint_id})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

@csrf_exempt
def search_complaint(request, cid):
    try:
        complaint = Complaint.objects.get(Complaint_id=cid)
        return JsonResponse({"found": True, "status": complaint.status_id.status_name, "title": complaint.title})
    except Complaint.DoesNotExist:
        return JsonResponse({"found": False})

@csrf_exempt
def student_complaints(request, roll, status):
    try:
        student = Student.objects.get(roll=roll)
        status_obj = Status.objects.get(status_name=status)
        complaints = Complaint.objects.filter(student_id=student, status_id=status_obj).order_by('-created_date')

        data = [{"id": c.Complaint_id, "title": c.title, "status": c.status_id.status_name, "category_name": c.cat_id.cat_name, "created_date": c.created_date.strftime("%B %d, %Y") if c.created_date else "N/A"} for c in complaints]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def staff_complaints(request, emp_id):
    try:
        staff = Staff.objects.get(emp_id=emp_id)
        if staff.hostel_id:
            complaints = Complaint.objects.filter(hostel_id=staff.hostel_id).order_by('-created_date')
        else:
            complaints = Complaint.objects.all().order_by('-created_date')

        data = [{"id": c.Complaint_id, "title": c.title, "status": c.status_id.status_name, "category_name": c.cat_id.cat_name, "created_date": c.created_date.strftime("%B %d, %Y") if c.created_date else "N/A"} for c in complaints]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def complaint_details(request, cid):
    try:
        c = Complaint.objects.get(Complaint_id=cid)
        workers = TechnicalWorker.objects.filter(cat_id=c.cat_id)
        worker_list = [{"name": w.name, "mobile": w.mobile} for w in workers]

        data = {
            "success": True,
            "id": c.Complaint_id,
            "title": c.title,
            "description": c.description,
            "status": c.status_id.status_name,
            "category": c.cat_id.cat_name,
            "created_date": c.created_date.strftime("%B %d, %Y - %I:%M %p") if c.created_date else "N/A",
            "solved_date": c.solved_date.strftime("%B %d, %Y - %I:%M %p") if c.solved_date else None,
            "student_name": c.student_id.name,
            "student_roll": c.student_id.roll,
            "student_mobile": c.student_id.mobile,
            "hostel": c.hostel_id.name,
            "workers": worker_list,
            "attachment_url": c.attachment.url if c.attachment else None,
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

@csrf_exempt   
def update_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        complaint = Complaint.objects.get(Complaint_id=data["id"])
        new_status, _ = Status.objects.get_or_create(status_name=data["status"])
        
        complaint.status_id = new_status
        if data["status"] == "Solved":
            complaint.solved_date = timezone.now()
            if "emp_id" in data:
                try:
                    staff = Staff.objects.get(emp_id=data["emp_id"])
                    complaint.solved_by = staff
                except Exception: pass
            
        complaint.save()
        return JsonResponse({"success": True})

# --- NEW: ADD TECHNICAL WORKER API ---
@csrf_exempt
def add_worker(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            # Find the category they selected
            category, _ = Category.objects.get_or_create(cat_name=data["category"])
            
            # Auto-generate a worker_id starting at 5000
            last_worker = TechnicalWorker.objects.order_by('-worker_id').first()
            new_id = (last_worker.worker_id + 1) if last_worker else 5000

            TechnicalWorker.objects.create(
                worker_id=new_id,
                name=data["name"],
                mobile=data["mobile"],
                cat_id=category
            )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
@csrf_exempt
def complaint_stats(request):
    total = Complaint.objects.count()
    pending = Complaint.objects.filter(status_id__status_name="Pending").count()
    progress = Complaint.objects.filter(status_id__status_name="In Progress").count()
    solved = Complaint.objects.filter(status_id__status_name="Solved").count()
    return JsonResponse({"total": total, "pending": pending, "progress": progress, "solved": solved})
# --- HTML PAGE VIEWS ---
def index_page(request): return render(request, 'index.html')
def login_page(request): return render(request, 'login.html')
def signin_page(request): return render(request, 'signin.html')
def student_page(request): return render(request, 'student.html')
def staff_page(request): return render(request, 'staff.html')
def complaint_page(request): return render(request, 'complaint.html')
def complaint_success(request): return render(request, 'complaint_success.html')
def change_password_page(request): return render(request, 'change_password.html')
