from django.urls import path
from .views import (
    WarehouseListCreateAPIView,
    WarehouseDetailAPIView
)

urlpatterns = [
    path("warehouse/", WarehouseListCreateAPIView.as_view(), name="Get All and Post"),
    path("warehouse/", WarehouseDetailAPIView.as_view(), name="Get One, Put And Delete")
]
