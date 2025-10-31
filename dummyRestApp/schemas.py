from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    inline_serializer,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample,
)
from rest_framework import serializers
from .serializers import WarehouseSerializer


# ============================================================
# 📦 SCHEMA UNTUK WAREHOUSE (List, Create, Retrieve, Update, Delete)
# ============================================================

warehouse_list_create_schema = extend_schema_view(
    # ----------------------------
    # GET (List all)
    # ----------------------------
    get=extend_schema(
        operation_id='warehouse_list',
        parameters=[
            OpenApiParameter(
                name='warehouse_name',
                description='Filter berdasarkan nama gudang (opsional)',
                required=False,
                type=str,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            200: WarehouseSerializer(many=True),
            404: OpenApiResponse(description="Data tidak ditemukan"),
        },
        description='Mengambil daftar semua Warehouse dengan opsi filter nama.',
    ),

    # ----------------------------
    # POST (Create)
    # ----------------------------
    post=extend_schema(
        operation_id='warehouse_create',
        request={
            'application/json': WarehouseSerializer,
            'multipart/form-data': WarehouseSerializer,
        },
        responses={
            201: inline_serializer(
                name="WarehouseCreateSuccessResponse",
                fields={
                    "status": serializers.IntegerField(
                        default=201,
                        help_text="HTTP status code hasil operasi."
                    ),
                    "message": serializers.CharField(
                        default="Data Warehouse berhasil dibuat."
                    ),
                    "data": WarehouseSerializer()
                }
            ),
            400: inline_serializer(
                name="WarehouseCreateErrorResponse",
                fields={
                    "status": serializers.CharField(default="error"),
                    "message": serializers.CharField(default="Validasi input gagal."),
                    "errors": serializers.JSONField(
                        help_text="Detail error validasi input."
                    ),
                }
            ),
        },
        description='Membuat Warehouse baru.',
        examples=[
            OpenApiExample(
                "Contoh Request JSON",
                summary="Contoh input JSON",
                value={
                    "warehouse_name": "Imah Aing",
                    "warehouse_location": "Jl. Sekeloa Gg.Loa 1 No 29 Bandung"
                },
                request_only=True,
            ),
            OpenApiExample(
                "Contoh Response Sukses",
                summary="Response sukses (201)",
                value={
                    "status": 201,
                    "message": "Data Warehouse berhasil dibuat.",
                    "data": {
                        "warehouse_name": "Imah Aing",
                        "warehouse_location": "Jl. Sekeloa Gg.Loa 1 No 29 Bandung"
                    }
                },
                response_only=True,
            ),
            OpenApiExample(
                "Contoh Response Gagal",
                summary="Response gagal validasi (400)",
                value={
                    "status": "error",
                    "message": "Validasi input gagal.",
                    "errors": {
                        "warehouse_name": ["Field ini wajib diisi."]
                    }
                },
                response_only=True,
            ),
        ],
    ),
)


# ============================================================
# 📦 SCHEMA UNTUK WAREHOUSE DETAIL (GET by ID, PUT, DELETE)
# ============================================================

warehouse_detail_schema = extend_schema_view(
    # ----------------------------
    # GET (Retrieve by ID)
    # ----------------------------
    get=extend_schema(
        operation_id='warehouse_retrieve',
        parameters=[
            OpenApiParameter(
                name='id',
                description='ID dari Warehouse',
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: WarehouseSerializer,
            404: OpenApiResponse(description="Warehouse tidak ditemukan"),
        },
        description='Mengambil detail Warehouse berdasarkan ID.',
    ),

    # ----------------------------
    # PUT (Update)
    # ----------------------------
    put=extend_schema(
        operation_id='warehouse_update',
        parameters=[
            OpenApiParameter(
                name='id',
                description='ID dari Warehouse yang akan diperbarui',
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            ),
        ],
        request={
            'application/json': WarehouseSerializer,
            'multipart/form-data': WarehouseSerializer,
        },
        responses={
            200: WarehouseSerializer,
            400: OpenApiResponse(description="Validasi input gagal."),
            404: OpenApiResponse(description="Warehouse tidak ditemukan."),
        },
        description='Memperbarui data Warehouse berdasarkan ID.',
    ),

    # ----------------------------
    # DELETE
    # ----------------------------
    delete=extend_schema(
        operation_id='warehouse_delete',
        parameters=[
            OpenApiParameter(
                name='id',
                description='ID dari Warehouse yang akan dihapus',
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            204: OpenApiResponse(description="Warehouse berhasil dihapus."),
            404: OpenApiResponse(description="Warehouse tidak ditemukan."),
        },
        description='Menghapus Warehouse berdasarkan ID.',
    ),
)
