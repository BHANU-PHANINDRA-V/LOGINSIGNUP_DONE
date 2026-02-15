from django.http import JsonResponse
from .models import Staff, Student
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body)

        Student.objects.create(
            roll=data["roll"],
            name=data["name"],
            mail=data["mail"],
            pswd=data["pswd"],
            mobile=data["mobile"]
        )

        return JsonResponse({"success":True})

#staff signup
@csrf_exempt
def staff_signup(request):
    if request.method == "POST":
        data = json.loads(request.body)

        category = Category.objects.get(cat_name=data["category"])

        staff = Staff.objects.create(
            name=data["name"],
            category=category,
            mail=data["mail"],
            mobile=data["mobile"],
            pswd=data["pswd"]
        )

        return JsonResponse({"success":True,
                            "emp_id": staff.emp_id 
                            })
    
@csrf_exempt
def staff_login(request):
    if request.method == "POST":
        data = json.loads(request.body)

        exists = Staff.objects.filter(
            emp_id=data["emp_id"],
            pswd=data["pswd"]
        ).exists()

        return JsonResponse({"success":exists})    
@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)

        exists = Student.objects.filter(
            roll=data["roll"],
            pswd=data["pswd"]
        ).exists()

        return JsonResponse({"success":exists})
#complaint register api
from django.http import JsonResponse
from .models import Complaint, Student, Category
import json
@csrf_exempt  #if it is not included it shows error of [14/Feb/2026 18:25:09] "POST /login/ HTTP/1.1" 200 17 Forbidden (Origin checking failed - http://
def register_complaint(request):
    if request.method == "POST":
        data = json.loads(request.body)

        student = Student.objects.get(roll=data["roll"])
        category = Category.objects.get(cat_name=data["category"])  

        complaint = Complaint.objects.create(
            title=data["title"],
            description=data["description"],
            category=category,
            student=student
        )

        return JsonResponse({
            "success": True,
            "complaint_id": complaint.id   #django automaticalky increments the id field for each new complaint
        })
#complaint search api
@csrf_exempt
def search_complaint(request, cid):
    try:
        complaint = Complaint.objects.get(id=cid)
        return JsonResponse({
            "found": True,
            "status": complaint.status,
            "title": complaint.title
        })
    except Complaint.DoesNotExist:
        return JsonResponse({"found": False})
#staff view api
@csrf_exempt
def staff_complaints(request, emp_id):
    from .models import Staff

    staff = Staff.objects.get(emp_id=emp_id)
    complaints = Complaint.objects.filter(category=staff.category)

    data = []
    for c in complaints:
        data.append({
            "id": c.id,
            "title": c.title,
            "status": c.status
        })

    return JsonResponse(data, safe=False)
#update complaint status api
@csrf_exempt   
def update_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        complaint = Complaint.objects.get(id=data["id"])
        complaint.status = data["status"]
        complaint.save()

        return JsonResponse({"success": True})
#complaint stats
from django.db.models import Count
from .models import Complaint
from django.http import JsonResponse
#@csrf_exempt
#def complaint_stats(request):
 #   total = Complaint.objects.count()
  #  solved = Complaint.objects.filter(status="Solved").count()
   # progress = Complaint.objects.filter(status="In Progress").count()
#
 #   return JsonResponse({
  #      "total": total,
   #     "solved": solved,
    #    "progress": progress
  #  })
@csrf_exempt
def complaint_stats(request):
    total = Complaint.objects.count()
    pending = Complaint.objects.filter(status="Pending").count()
    progress = Complaint.objects.filter(status="In Progress").count()
    solved = Complaint.objects.filter(status="Solved").count()

    return JsonResponse({
        "total": total,
        "pending": pending,
        "progress": progress,
        "solved": solved
    })
