from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DummyWarehouse
from .serializers import WarehouseSerializer
from django.shortcuts import get_object_or_404
from .schemas import (
    warehouse_list_create_schema,
    warehouse_detail_schema
)


@warehouse_list_create_schema
class WarehouseListCreateAPIView(APIView):
    """
    GET: List all warehouses (dengan filter optional query param)
    POST: Create new warehouse (JSON atau multipart/form-data)
    """

    def get(self, request):
        # Optional filter query
        name_filter = request.query_params.get('warehouse_name')
        queryset = DummyWarehouse.objects.all()
        if name_filter:
            queryset = queryset.filter(warehouse_name__icontains=name_filter)
        serializer = WarehouseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WarehouseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": status.HTTP_201_CREATED,
                "message": "Data Warehouse berhasil dibuat.",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data = {
            "status": "error",
            "message": "Validasi input gagal.",
            "errors": serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@warehouse_detail_schema
class WarehouseDetailAPIView(APIView):
    """
    GET: Retrieve warehouse by ID
    PUT: Update warehouse by ID (JSON or multipart/form-data)
    DELETE: Delete warehouse by ID
    """

    def get(self, request, id):
        warehouse = get_object_or_404(DummyWarehouse, id=id)
        serializer = WarehouseSerializer(warehouse)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        warehouse = get_object_or_404(DummyWarehouse, id=id)
        serializer = WarehouseSerializer(warehouse, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Validasi input gagal.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        warehouse = get_object_or_404(DummyWarehouse, id=id)
        warehouse.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
