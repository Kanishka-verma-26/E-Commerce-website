import graphene
from graphene_django import DjangoObjectType

from.models import Product,ProductImage, Category

class ProductImageType(DjangoObjectType):
    class Meta:
        model = ProductImage
        field = ('id','image','alt_text')

    def resolve_image(self,info):
        if self.image:
            self.image = info.context.build_absolute_uri(self.image.url)            # build_absolute_uri will fetch the address of our system that we are sticking together with the image url
        return self.image


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id","title","description",'regular_price','slug',"product_image")    # referring the ProductImageType because related_name="product_image"



class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id','name',"category",'parent',"level","slug")          # related_name = "category



class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)       # graphene.List will view all the Products in a list

    """collecting an individual item from the databse"""
    all_products_by_name = graphene.Field(ProductType, slug=graphene.String(required=True))             # as we are returning one item so we will utilise graphene.Field; we are defining a string 'slug' so that we can run query for a particular item

    """collecting products based on category"""
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    all_Categories = graphene.List(CategoryType)           # display all categories based on defined level

    all_categories_by_level = graphene.List(CategoryType, level = graphene.Int(required=True))          # display all categories based on user input level

    def resolve_all_categories_by_level(root,info,level):
        try:
            return Category.objects.filter(level=level)
        except Category.DoesNotExist:
            return None


    def resolve_category_by_name(root,info,name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None


    def resolve_all_products_by_name(root,info,slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return None


    def resolve_all_products(root,info):
        print("printing")
        return Product.objects.all()


    def resolve_all_Categories(root, info):
        return Category.objects.filter(level=0)

schema = graphene.Schema(query=Query)



