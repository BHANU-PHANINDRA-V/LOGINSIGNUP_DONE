from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grievance', '0003_complaint_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
