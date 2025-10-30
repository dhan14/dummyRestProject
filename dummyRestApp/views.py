from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import (
    DummyWarehouse,
)
from .serializers import (
    WarehouseSerializer,
)


class WarehouseListCreateAPIView(APIView):
    def get(self, request):
        warehouse = DummyWarehouse.objects.all()
        w_serializer = WarehouseSerializer(warehouse, many=True)
        return Response(w_serializer.data, status=status.HTTP_200_OK)
