from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='get',
    operation_description="Список продуктов с фильтрацией по категории",
    manual_parameters=[
        openapi.Parameter('category_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="ID категории")
    ],
    responses={200: ProductSerializer(many=True)}
)
@api_view(['GET'])
def product_list(request):
    category_id = request.GET.get('category_id')
    products = Product.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Создать продукт с изображениями",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'description', 'category_id', 'uploaded_images'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'category_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'uploaded_images': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_FILE)
            )
        }
    ),
    consumes=['multipart/form-data'],
    responses={201: ProductSerializer}
)
@api_view(['POST'])
def product_create(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='patch',
    operation_description="Обновить продукт с изображениями и категорией",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'category_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'uploaded_images': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_FILE)
            )
        }
    ),
    consumes=['multipart/form-data'],
    responses={200: ProductSerializer, 404: 'Not Found'}
)
@api_view(['PATCH'])
def product_update(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
