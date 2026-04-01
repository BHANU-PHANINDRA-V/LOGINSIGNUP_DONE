from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grievance', '0002_staff_first_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='complaint_images/'),
        ),
    ]
