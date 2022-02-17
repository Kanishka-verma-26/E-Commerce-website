from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin       # to register MPTTModel

# Register your models here.
admin.site.register(Category,MPTTModelAdmin)

class ProductSpeciicationInline(admin.TabularInline):           # "TabularInline" means inline in table  format
    model = ProductSpecification

@admin.register(ProductType)
class ProductTypeInline(admin.ModelAdmin):
    inlines = [                                     # The admin interface has the ability to edit models on the same page as a parent model. These are called inlines.
        ProductSpeciicationInline                       # now you have ProductSpecification model inside ProductType
    ]
class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationValueInline,                    # now we will have "ProductSpecificationValue" and "ProductImage" inside "product"
        ProductImageInline
    ]
# admin.site.register(Category,MPTTModelAdmin)

