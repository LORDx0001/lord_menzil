from rest_framework import serializers
from .models import Product, ProductImage, ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'category_id', 'images', 'uploaded_images']

    def create(self, validated_data):
        images = validated_data.pop('uploaded_images', [])
        category_id = validated_data.pop('category_id')
        product = Product.objects.create(**validated_data, category_id=category_id)
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return product

    def update(self, instance, validated_data):
        images = validated_data.pop('uploaded_images', [])
        category_id = validated_data.pop('category_id', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if category_id:
            instance.category_id = category_id
        instance.save()

        for image in images:
            ProductImage.objects.create(product=instance, image=image)
        return instance
