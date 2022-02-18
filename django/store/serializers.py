from rest_framework import serializers

from .models import Product,ProductImage,Category

"""
 Serializer is a tool that can convert our complex data models into native Python datatypes.
 It is very useful because it can be easily converted into JSON.
 
 (serializers allow us to format the collected data to send it across the frontend)
"""

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id","image","alt_text"]


class ProductSerializer(serializers.ModelSerializer):
    product_image = ImageSerializer(many=True, read_only=True)          # through this we can also call the images of the product

    class Meta:
        model = Product
        fields = ["id","category",'slug',"title","description","regular_price","product_image"]               # in fields we define data that we want to collect


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug"]
