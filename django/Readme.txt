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


