from django.urls import path
from .views import (
    WarehouseListCreateAPIView
)

urlpatterns = [
    path("warehouse/", WarehouseListCreateAPIView.as_view(), name="Get")
]
