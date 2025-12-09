from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from tenants.models import Municipality


class Command(BaseCommand):
    help = "Cria municípios e usuários de teste com credenciais padrão."

    def handle(self, *args, **options):
        User = get_user_model()

        municipalities_data = [
            {
                "key": "central",
                "name": "Prefeitura Central",
                "cnpj": "10.000.000/0001-10",
                "address": "Av. Central, 100",
                "city": "Sao Paulo",
                "state": "SP",
                "phone": "11999990000",
            },
            {
                "key": "interior",
                "name": "Prefeitura Interior",
                "cnpj": "20.000.000/0001-20",
                "address": "Av. das Flores, 200",
                "city": "Campinas",
                "state": "SP",
                "phone": "11988880000",
            },
        ]

        municipalities = {}
        for muni in municipalities_data:
            obj, created = Municipality.objects.update_or_create(
                cnpj=muni["cnpj"],
                defaults={
                    "name": muni["name"],
                    "address": muni["address"],
                    "city": muni["city"],
                    "state": muni["state"],
                    "phone": muni["phone"],
                },
            )
            municipalities[muni["key"]] = obj
            status = "criado" if created else "atualizado"
            self.stdout.write(self.style.SUCCESS(f"Municipio {obj.name} {status}."))

        users_data = [
            {
                "email": "superadmin@example.com",
                "password": "pass123",
                "role": User.Roles.SUPERADMIN,
                "municipality": None,
                "first_name": "Super",
                "last_name": "Admin",
            },
            {
                "email": "admin@central.gov",
                "password": "pass123",
                "role": User.Roles.ADMIN_MUNICIPALITY,
                "municipality": municipalities["central"],
                "first_name": "Admin",
                "last_name": "Central",
            },
            {
                "email": "operador@central.gov",
                "password": "pass123",
                "role": User.Roles.OPERATOR,
                "municipality": municipalities["central"],
                "first_name": "Operador",
                "last_name": "Central",
            },
            {
                "email": "visualizador@central.gov",
                "password": "pass123",
                "role": User.Roles.VIEWER,
                "municipality": municipalities["central"],
                "first_name": "Viewer",
                "last_name": "Central",
            },
            {
                "email": "admin@interior.gov",
                "password": "pass123",
                "role": User.Roles.ADMIN_MUNICIPALITY,
                "municipality": municipalities["interior"],
                "first_name": "Admin",
                "last_name": "Interior",
            },
            {
                "email": "operador@interior.gov",
                "password": "pass123",
                "role": User.Roles.OPERATOR,
                "municipality": municipalities["interior"],
                "first_name": "Operador",
                "last_name": "Interior",
            },
            {
                "email": "visualizador@interior.gov",
                "password": "pass123",
                "role": User.Roles.VIEWER,
                "municipality": municipalities["interior"],
                "first_name": "Viewer",
                "last_name": "Interior",
            },
        ]

        for user_data in users_data:
            password = user_data["password"]
            email = user_data["email"]
            defaults = {k: v for k, v in user_data.items() if k != "password"}
            user, created = User.objects.update_or_create(email=email, defaults=defaults)
            user.set_password(password)
            user.save()
            status = "criado" if created else "atualizado"
            self.stdout.write(self.style.SUCCESS(f"Usuario {email} {status} com senha padrao."))

        self.stdout.write(self.style.WARNING("Senha padrao para todos: pass123"))
