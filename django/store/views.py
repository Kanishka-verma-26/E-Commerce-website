from django.shortcuts import render
from rest_framework import generics
from . import models
from .models import Category, Product
from .serializers import *


class ProductListView(generics.ListAPIView):
    """ ListAPIView is Used for read-only endpoints to
    represent a collection of model instances."""

    queryset = Product.objects.all()                # we tell django what data do we need using 'queryset'
    serializer_class = ProductSerializer            # serializers allow us to format the collected data to send it across the frontend

class Product(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryItemView(generics.ListAPIView):           # presenting the products according to their categories
    serializer_class = ProductSerializer

    def get_queryset(self):
        return models.Product.objects.filter(category__slug=self.kwargs["slug"])            # this will only show the products of the particular category on the frontend

        # return models.Product.objects.filter(category__slug=self.kwargs["slug"]).self_descendants(include_self=True)              # this will show the  products of the child category also on the frontend



class CategoryListView(generics.ListAPIView):           # represent all the categories
    queryset = Category.objects.filter(level=1)         # here level is similar to tree levels (level 0 has men and women; and till now level 1 has clothes,shoes, bags, active_wear, footwear; lvl 2 has boots)
    serializer_class = CategorySerializer