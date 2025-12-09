import datetime
from rest_framework import serializers
from fleet.models import Vehicle, VehicleMaintenance, FuelLog


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {"municipality": {"read_only": True}}

    def validate_year(self, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("Ano do veículo não pode estar no futuro.")
        return value

    def validate(self, attrs):
        odometer_current = attrs.get("odometer_current", getattr(self.instance, "odometer_current", 0))
        odometer_initial = attrs.get("odometer_initial", getattr(self.instance, "odometer_initial", 0))
        if odometer_current < odometer_initial:
            raise serializers.ValidationError("Quilometragem atual não pode ser menor que a inicial.")
        return attrs


class VehicleMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleMaintenance
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


class FuelLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelLog
        fields = "__all__"
        read_only_fields = ["id", "created_at", "municipality"]
        extra_kwargs = {"receipt_image": {"required": False}}

    def validate(self, attrs):
        request = self.context.get("request")
        portal_driver = self.context.get("portal_driver")
        user = getattr(request, "user", None)
        driver = attrs.get("driver", getattr(self.instance, "driver", None))
        vehicle = attrs.get("vehicle", getattr(self.instance, "vehicle", None))
        liters = attrs.get("liters", getattr(self.instance, "liters", 0))

        if liters is not None and liters <= 0:
            raise serializers.ValidationError("Quantidade de litros deve ser maior que zero.")

        if driver and vehicle and driver.municipality_id != vehicle.municipality_id:
            raise serializers.ValidationError("Motorista e veículo precisam ser da mesma prefeitura.")

        if portal_driver:
            if driver and driver.id != portal_driver.id:
                raise serializers.ValidationError("Motorista inválido para este token.")
            if vehicle and vehicle.municipality_id != portal_driver.municipality_id:
                raise serializers.ValidationError("Veículo precisa pertencer à prefeitura do motorista.")
            attrs["driver"] = portal_driver
            attrs["municipality"] = portal_driver.municipality
            return attrs

        if user and getattr(user, "role", None) != "SUPERADMIN":
            if driver and driver.municipality_id != user.municipality_id:
                raise serializers.ValidationError("Motorista precisa pertencer à prefeitura do usuário.")
            if vehicle and vehicle.municipality_id != user.municipality_id:
                raise serializers.ValidationError("Veículo precisa pertencer à prefeitura do usuário.")
        return attrs
