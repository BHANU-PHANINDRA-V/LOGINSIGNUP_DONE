from django.db import migrations


def seed_hostels(apps, schema_editor):
    Hostel = apps.get_model("grievance", "Hostel")

    hostel_plan = [
        (3, "Sabari"),
        (4, "Swarnamukhi"),
        (5, "Godavari"),
    ]

    for preferred_id, hostel_name in hostel_plan:
        if Hostel.objects.filter(name=hostel_name).exists():
            continue

        hostel_id = preferred_id
        while Hostel.objects.filter(hostel_id=hostel_id).exists():
            hostel_id += 1

        Hostel.objects.create(hostel_id=hostel_id, name=hostel_name)


def remove_seeded_hostels(apps, schema_editor):
    Hostel = apps.get_model("grievance", "Hostel")
    Hostel.objects.filter(name__in=["Sabari", "Swarnamukhi", "Godavari"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("grievance", "0006_normalize_category_ids"),
    ]

    operations = [
        migrations.RunPython(seed_hostels, remove_seeded_hostels),
    ]
