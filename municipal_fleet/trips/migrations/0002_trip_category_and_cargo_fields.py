from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trips", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="trip",
            name="cargo_description",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="trip",
            name="cargo_purpose",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="trip",
            name="cargo_quantity",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="trip",
            name="cargo_size",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="trip",
            name="category",
            field=models.CharField(
                choices=[
                    ("PASSENGER", "Passageiro"),
                    ("OBJECT", "Objeto"),
                    ("MIXED", "Passageiro e Objeto"),
                ],
                default="PASSENGER",
                max_length=20,
            ),
        ),
    ]
