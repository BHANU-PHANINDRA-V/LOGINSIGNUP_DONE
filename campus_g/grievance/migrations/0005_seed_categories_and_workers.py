from django.db import migrations


def seed_categories_and_workers(apps, schema_editor):
    Category = apps.get_model("grievance", "Category")
    TechnicalWorker = apps.get_model("grievance", "TechnicalWorker")

    category_plan = [
        (101, "Electrical"),
        (102, "Plumbing"),
        (103, "Carpentry"),
        (104, "Internet & Network"),
    ]

    def ensure_category(preferred_id, cat_name):
        existing = Category.objects.filter(cat_name=cat_name).first()
        if existing:
            return existing

        category_id = preferred_id
        while Category.objects.filter(cat_id=category_id).exists():
            category_id += 1

        return Category.objects.create(cat_id=category_id, cat_name=cat_name)

    categories = {
        cat_name: ensure_category(preferred_id, cat_name)
        for preferred_id, cat_name in category_plan
    }

    worker_plan = [
        ("Aarav Sharma", "9000000001", "Electrical"),
        ("Vivaan Patel", "9000000002", "Electrical"),
        ("Aditya Rao", "9000000003", "Electrical"),
        ("Krish Nair", "9000000004", "Electrical"),
        ("Arjun Mehta", "9000000005", "Electrical"),
        ("Sai Prakash", "9000000006", "Electrical"),
        ("Rahul Verma", "9000000007", "Electrical"),
        ("Nikhil Das", "9000000008", "Electrical"),
        ("Rohan Singh", "9000000009", "Plumbing"),
        ("Karthik Iyer", "9000000010", "Plumbing"),
        ("Manoj Kumar", "9000000011", "Plumbing"),
        ("Deepak Yadav", "9000000012", "Plumbing"),
        ("Surya Teja", "9000000013", "Plumbing"),
        ("Harish Reddy", "9000000014", "Plumbing"),
        ("Vinay Joshi", "9000000015", "Plumbing"),
        ("Tarun Mishra", "9000000016", "Plumbing"),
        ("Praveen Gupta", "9000000017", "Carpentry"),
        ("Sandeep Roy", "9000000018", "Carpentry"),
        ("Ajay Thakur", "9000000019", "Carpentry"),
        ("Mohan Lal", "9000000020", "Carpentry"),
        ("Yash Malhotra", "9000000021", "Carpentry"),
        ("Lokesh Jain", "9000000022", "Carpentry"),
        ("Pavan Babu", "9000000023", "Carpentry"),
        ("Anil Sahu", "9000000024", "Internet & Network"),
        ("Gautham Raj", "9000000025", "Internet & Network"),
        ("Srinivas Rao", "9000000026", "Internet & Network"),
        ("Ashwin Pillai", "9000000027", "Internet & Network"),
        ("Dinesh Paul", "9000000028", "Internet & Network"),
        ("Imran Khan", "9000000029", "Internet & Network"),
        ("Joseph Mathew", "9000000030", "Internet & Network"),
    ]

    next_worker_id = max(
        TechnicalWorker.objects.order_by("-worker_id").values_list("worker_id", flat=True).first() or 4999,
        4999,
    ) + 1

    for name, mobile, cat_name in worker_plan:
        if TechnicalWorker.objects.filter(name=name, mobile=mobile).exists():
            continue

        while TechnicalWorker.objects.filter(worker_id=next_worker_id).exists():
            next_worker_id += 1

        TechnicalWorker.objects.create(
            worker_id=next_worker_id,
            name=name,
            mobile=mobile,
            cat_id=categories[cat_name],
        )
        next_worker_id += 1


def remove_seeded_workers(apps, schema_editor):
    Category = apps.get_model("grievance", "Category")
    TechnicalWorker = apps.get_model("grievance", "TechnicalWorker")

    seeded_worker_names = [
        "Aarav Sharma", "Vivaan Patel", "Aditya Rao", "Krish Nair", "Arjun Mehta",
        "Sai Prakash", "Rahul Verma", "Nikhil Das", "Rohan Singh", "Karthik Iyer",
        "Manoj Kumar", "Deepak Yadav", "Surya Teja", "Harish Reddy", "Vinay Joshi",
        "Tarun Mishra", "Praveen Gupta", "Sandeep Roy", "Ajay Thakur", "Mohan Lal",
        "Yash Malhotra", "Lokesh Jain", "Pavan Babu", "Anil Sahu", "Gautham Raj",
        "Srinivas Rao", "Ashwin Pillai", "Dinesh Paul", "Imran Khan", "Joseph Mathew",
    ]
    seeded_categories = ["Electrical", "Plumbing", "Carpentry", "Internet & Network"]

    TechnicalWorker.objects.filter(name__in=seeded_worker_names).delete()
    Category.objects.filter(cat_name__in=seeded_categories, technicalworker__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("grievance", "0004_complaint_cost"),
    ]

    operations = [
        migrations.RunPython(seed_categories_and_workers, remove_seeded_workers),
    ]
