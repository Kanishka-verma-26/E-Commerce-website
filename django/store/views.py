from django.shortcuts import render
from rest_framework import generics

from .models import *
from .serializers import *


class ProductListView(generics.ListAPIView):
    """ ListAPIView is Used for read-only endpoints to
    represent a collection of model instances."""

    queryset = Product.objects.all()                # we tell django what data do we need using 'queryset'
    serializer_class = ProductSerializer            # serializers allow us to format the collected data to send it across the frontend