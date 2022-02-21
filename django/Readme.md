

                                            <h1>DRF (Django Rest Framework)</h1>




1) after successfully creating project, app and adding your app in your INSTALLED_APPS of settings.py, install black
            "pip install black"

            Black is the uncompromising Python code formatter. By using it, you agree to cede control over minutiae of hand-formatting.
            In return, Black gives you speed, determinism, and freedom from pycodestyle nagging about formatting.
            You will save time and mental energy for more important matters.


2) pip install isort
            its gonna sort out all your imports alphabetically, and automatically separated into sections and by type; which is going to follow the pepe stylings guidelines for python; i.e. given by above command


3) pip install pillow; bcoz we will be using images


4) pip install django-mptt; add 'mptt' in your INSTALLED_APPS
            Utilities for implementing Modified Preorder Tree Traversal with your Django Models and working with trees of Model instances.

            MPTT is a technique for storing hierarchical data in a database. The aim is to make retrieval operations very efficient.

            The trade-off for this efficiency is that performing inserts and moving items around the tree is more involved,
            as there's some extra work required to keep the tree structure in a good state at all times.

5) Build database

            * import all
                    from django.urls import reverse
                    from django.utils.translation import gettext_lazy as _
                    from mptt.models import MPTTModel, TreeForeignKey

            * build models for
                    * Products
                    * Categories (mptt)
                            in an ecommerce website we may have multiple layers such as we have shoes and there are multiple types of shoes and there can be multiple sizes for a particular type and the simplest way of managing that is by utilizing 'mptt'
                    * ProductType
                    * ProductSpecification
                    * ProductSpecificationValue
                    * ProductImage
                            ( we might need multiple images per product, so we couldn't store multiple images on the same product table, so we will be making the interaction here using 'is_feature' )

            * set up the media folder
                    different products will have different types of images ; directly link your ProductImage model to media folder so that every image uploaded their can be stroed into media not in the db

                    setup in settings.py
                             MEDIA_URL = "/media/"
                             MEDIA_ROOT = BASE_DIR / "media/"

6) set up the urls

            from django.conf import settings
            from django.conf.urls.static import static      # Helper function to return a URL pattern for serving files in debug mode

            if settings.DEBUG:
                urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

7) register your model; migrate; add some data through admin section

8) Django DRF

            * Configure DRF

                        Django DRF is a package that allow us to convert our application into an API ( for  example in this project next js can access the data in the database through django )

                        1) pip install djangorestframework
                        2) add 'rest_framework' into INSTALLED_APPS
                        3) give permission for accessing information, add the below in settings.py

                                        REST_FRAMEWORK = {
                                                'DEFAULT_PERMISSION_CLASSES': [
                                                    'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
                                                ]
                                            }

            * set URLS

            * define Views

            * define Serializers
                        ( serializers format the required data from the database in a way that it can be use for the frontend )

                        now if you run "http://127.0.0.1:8000/api/" you can see lists of Products in DRF





                                                GraphQL




( yes its a fact that you can work with Django DRF and GraphQL at the same time)

*** The one of the biggest changes using graphQL over Django DRF is that;
            in GraphqL we create queries on the front end so that gives us better control of what data we want to collect from our backend and even if we want to make changes in our data, we can simply achieve it from our frontend by changing query
            whereas in Django DRF we have to set out urls where all the data can be found and if you want to make a change in the data, then you have to make a change in both frontend and backend
        """

1) setup GraphQL

            * install the graphene-django package, it allows us to utilize graph in our django application
                                pip install graphene-django

            * add 'graphene_django' into your INSTALLED_APPS

            * setup your schema
                                GRAPHENE = {
                                    "SCHEMA": "store.schema.schema"         # store is my app name
                                }

            * create a new file as "schema.py" in your app folder


2) build schema

            * setup your url
                        import the  following
                                from graphene_django.views import GraphQLView
                                from django.views.decorators.csrf import csrf_exempt                ( Normally when you make a request via a form you want the form being submitted to your view to originate from your website and not come from some other domain. To ensure that this happens, you can put a csrf token in your form for your view to recognize. If you add @csrf_exempt to the top of your view, then you are basically telling the view that it doesn't need the token. This is a security exemption that you should take seriously.)

                        set the path
                                "path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),"


            * schema file
                        import graphene
                        from graphene_django import DjangoObjectType            ( Graphene-Django ships with a special DjangoObjectType that automatically transforms a Django Model into a ObjectType for you. )

            * import models you want to access                  ( as product_image is the foreign key of Product so if we want to display the product image into out query, we need to call product_image class also )

            * write classes for models                          ( also writing foreignkey product_image class to access it inside product query )
                            class ProductImageType(DjangoObjectType):
                                class Meta:
                                    model = ProductImage
                                    field = ('id','image','alt_text')


                            class ProductType(DjangoObjectType):
                                class Meta:
                                    model = Product
                                    fields = ("id","title","description",'regular_price','slug',"product_image")


            * write Query class to connect your data with 'resolve' function    ( Query helps us to access data using graphene.ObjectType, resolve is basically a query that we want to run or an action we want to take )

                          class Query(graphene.ObjectType):
                                all_products = graphene.List(ProductType)

                                def resolve_all_products(root,info):
                                    return Product.objects.all()

            * connect your query to schema
                          schema = graphene.Schema(query=Query)

            ( now we can run our query )
                            """"
                                query{
                                  allProducts{
                                    id
                                    title
                                    description
                                    productImage{
                                      id
                                      image
                                      altText
                                    }
                                  }
                                }
                            """"

            (as soon as we run the above query the image variable will return the link to the image which isn't even the full link and because of that when we gonna send this across the frontend its not gonna work; so now we need to actally build this link to the image )


            * build the link to the image

                            """"
                                def resolve_image(self,info):
                                    if self.image:
                                        self.image = info.context.build_absolute_uri(self.image.url)            # build_absolute_uri will fetch the address of our system that we are sticking together with the image url
                                    return self.image
                            """"

            ( now if we run our query we will get the fully qualified link such as "http://127.0.0.1:8000/media/images/heels.jpg" )


3) schema for an individual item


            * now if we want to collect an individual item from our database we need to create a new query reference

                              all_products_by_name = graphene.Field(ProductType, slug=graphene.String(required=True))           # as we are returning one item so we will utilise graphene.Field; we are defining a string 'slug' so that we can run query for a particular item by passing the parameter within query


            * resolve the above query for a particular string

                            """"
                                def resolve_all_products_by_name(root,info,slug):
                                    try:
                                        return Product.objects.get(slug=slug)
                                    except Product.DoesNotExist:
                                        return None
                            """"

            ( now we can run our query )
                            """"
                                query{
                                  allProductsByName(slug:"footwear"){
                                    id
                                    title
                                    description
                                    regularPrice
                                    productImage {
                                      id
                                      image
                                      altText
                                    }
                                  }
                                }
                            """"


4) schema to show products based on category

            * create class for CategoryType

            * write query and resolve function for CategoryType

            ( now we can run our query )

                            """"
                                query{
                                  categoryByName(name:"boots"){
                                    id
                                    name
                                    parent {
                                      id
                                      name
                                    }
                                    category {
                                      id
                                      title
                                      description
                                      regularPrice
                                      productImage{
                                        image
                                        altText
                                      }
                                    }
                                  }
                                }
                            """"



5) show categories in menu

            ( as we are using mptt through which we can categorise our products in levels, we can also display the categories based on levels )

            * to display categories based on levels; add "level" attribute into the fields of CategoryType class

                            """"
                                class CategoryType(DjangoObjectType):
                                    class Meta:
                                        model = Category
                                        fields = ('id','name',"category",'parent',"level")
                            """"
            * categories on user defined level

                            * write query and resolve function for CategoryType

                                        all_Categories = graphene.List(CategoryType)

                                            def resolve_all_Categories(root, info):
                                                    return Category.objects.filter(level=1)

                            ( now you can run the query )

                                            """"
                                                query{
                                                  allCategories{
                                                    id
                                                    slug
                                                    name
                                                  }
                                                }
                                            """"

            * categories on user input level

                            * write query and resolve function for CategoryType

                                        all_categories_by_level = graphene.List(CategoryType, level = graphene.Int(required=True))          # display all categories based on user input level

                                        def resolve_all_categories_by_level(root,info,level):
                                            try:
                                                return Category.objects.filter(level=level)
                                            except Category.DoesNotExist:
                                                return None

                            ( now you can run the query )

                                        """"
                                            query{
                                              allCategoriesByLevel(level:1){
                                                id
                                                slug
                                                name
                                              }
                                            }
                                        """"
