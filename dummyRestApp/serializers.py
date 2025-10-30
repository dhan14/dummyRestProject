from rest_framework import serializers
from .models import (
    DummyWarehouse,
    DummyInventory,
    DummyProduct,
    DummyStockMovement
)


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DummyWarehouse
        fields = [
            'warehouse_name',
            'warehouse_location',
        ]
