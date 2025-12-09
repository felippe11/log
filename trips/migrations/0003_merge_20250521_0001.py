from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("trips", "0002_trip_category_and_cargo_fields"),
        ("trips", "0002_trip_passengers_details"),
    ]

    operations = []
