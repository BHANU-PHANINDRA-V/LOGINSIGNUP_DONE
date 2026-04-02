from django.db import migrations


def normalize_category_ids(apps, schema_editor):
    Category = apps.get_model("grievance", "Category")
    TechnicalWorker = apps.get_model("grievance", "TechnicalWorker")
    Complaint = apps.get_model("grievance", "Complaint")

    category_targets = [
        ("Plumbing", 4),
        ("Carpentry", 5),
        ("Internet & Network", 6),
    ]

    worker_category_map = {
        "Rohan Singh": "Plumbing",
        "Karthik Iyer": "Plumbing",
        "Manoj Kumar": "Plumbing",
        "Deepak Yadav": "Plumbing",
        "Surya Teja": "Plumbing",
        "Harish Reddy": "Plumbing",
        "Vinay Joshi": "Plumbing",
        "Tarun Mishra": "Plumbing",
        "Praveen Gupta": "Carpentry",
        "Sandeep Roy": "Carpentry",
        "Ajay Thakur": "Carpentry",
        "Mohan Lal": "Carpentry",
        "Yash Malhotra": "Carpentry",
        "Lokesh Jain": "Carpentry",
        "Pavan Babu": "Carpentry",
        "Anil Sahu": "Internet & Network",
        "Gautham Raj": "Internet & Network",
        "Srinivas Rao": "Internet & Network",
        "Ashwin Pillai": "Internet & Network",
        "Dinesh Paul": "Internet & Network",
        "Imran Khan": "Internet & Network",
        "Joseph Mathew": "Internet & Network",
    }

    for category_name, target_id in category_targets:
        current = Category.objects.filter(cat_name=category_name).first()
        target = Category.objects.filter(cat_id=target_id).first()

        if target and target.cat_name == category_name:
            destination = target
        elif not target:
            destination = Category.objects.create(cat_id=target_id, cat_name=category_name)
        else:
            continue

        if current and current.cat_id != destination.cat_id:
            TechnicalWorker.objects.filter(cat_id=current).update(cat_id=destination)
            Complaint.objects.filter(cat_id=current).update(cat_id=destination)
            current.delete()

    categories_by_name = {
        category.cat_name: category
        for category in Category.objects.filter(
            cat_name__in=[name for name, _ in category_targets]
        )
    }

    for worker_name, category_name in worker_category_map.items():
        category = categories_by_name.get(category_name)
        if category:
            TechnicalWorker.objects.filter(name=worker_name).update(cat_id=category)


def reverse_normalize_category_ids(apps, schema_editor):
    Category = apps.get_model("grievance", "Category")
    TechnicalWorker = apps.get_model("grievance", "TechnicalWorker")
    Complaint = apps.get_model("grievance", "Complaint")

    reverse_targets = [
        ("Plumbing", 102),
        ("Carpentry", 103),
        ("Internet & Network", 104),
    ]

    for category_name, old_id in reverse_targets:
        current = Category.objects.filter(cat_name=category_name).first()
        old_category = Category.objects.filter(cat_id=old_id).first()

        if old_category and old_category.cat_name == category_name:
            destination = old_category
        elif not old_category:
            destination = Category.objects.create(cat_id=old_id, cat_name=category_name)
        else:
            continue

        if current and current.cat_id != destination.cat_id:
            TechnicalWorker.objects.filter(cat_id=current).update(cat_id=destination)
            Complaint.objects.filter(cat_id=current).update(cat_id=destination)
            current.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("grievance", "0005_seed_categories_and_workers"),
    ]

    operations = [
        migrations.RunPython(normalize_category_ids, reverse_normalize_category_ids),
    ]
