from rest_framework import serializers

from .models import Product

"""
 Serializer is a tool that can convert our complex data models into native Python datatypes.
 It is very useful because it can be easily converted into JSON.
 
 (serializers allow us to format the collected data to send it across the frontend)
"""

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","title","description"]               # in fields we define data that we want to collect