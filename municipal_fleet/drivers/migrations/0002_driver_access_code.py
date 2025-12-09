from django.db import migrations, models
import drivers.models


class Migration(migrations.Migration):
    dependencies = [
        ("drivers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="driver",
            name="access_code",
            field=models.CharField(default=drivers.models.generate_access_code, max_length=20, unique=True),
        ),
    ]
