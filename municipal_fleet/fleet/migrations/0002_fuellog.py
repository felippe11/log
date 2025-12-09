from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tenants", "0001_initial"),
        ("drivers", "0002_driver_access_code"),
        ("fleet", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FuelLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("filled_at", models.DateField()),
                ("liters", models.DecimalField(decimal_places=2, max_digits=8)),
                ("fuel_station", models.CharField(max_length=255)),
                ("receipt_image", models.FileField(blank=True, null=True, upload_to="fuel_receipts/")),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "driver",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="fuel_logs", to="drivers.driver"),
                ),
                (
                    "municipality",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="fuel_logs", to="tenants.municipality"),
                ),
                (
                    "vehicle",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="fuel_logs", to="fleet.vehicle"),
                ),
            ],
            options={
                "ordering": ["-filled_at", "-created_at"],
            },
        ),
    ]
