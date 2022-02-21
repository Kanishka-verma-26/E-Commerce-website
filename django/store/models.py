from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey               # "MPTT" is a technique for storing hierarchical data in a database and "TreeForeignKey" is just like a regular ForeignKey but it makes the default form field display choices in tree form

# Create your models here.

class Category(MPTTModel):
    """ Category table implemented with MPTT"""

    name = models.CharField(verbose_name = _("Category Name"), help_text= _("Required and Unique"), max_length=255, unique=True,)
    slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=255, unique=True)                                               # SlugField (source code) is a field for storing URL slugs in a relational database.
    parent = TreeForeignKey("self",on_delete = models.CASCADE, null=True, blank= True, related_name="children")                             # TreeForeignKey is just a regular ForeignKey that renders form fields differently in the admin and a few other places; it will build the hierarchical structure for the categories
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]           # indicates the natural ordering of the data in the tree.

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("store:category_list",args=[self.slug])

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """ ProductType table will provide a list of the different types
     of products that are for sale """

    name = models.CharField(verbose_name=_("Product Name"), help_text=_("Required"), max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """ The product specification table contains product
    specifications or features for the product type """

    product_type = models.ForeignKey(ProductType,on_delete=models.RESTRICT)         # RESTRICT- Prevent deletion of the referenced object by raising RestrictedError
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=250)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name

class Product(models.Model):
    """ this table contains all product items """

    product_type = models.ForeignKey(ProductType,on_delete=models.RESTRICT)
    category = models.ForeignKey(Category,on_delete=models.RESTRICT, related_name="category")
    title = models.CharField(verbose_name=_("title"),help_text=_("Required"),max_length=255)
    description = models.TextField(verbose_name=_("description"),help_text=_("Not Required"),blank=True)
    slug = models.SlugField(max_length=250)
    regular_price = models.DecimalField(verbose_name=_("Regular Price"),help_text=_("Maximum 999.99"),
                                        error_messages={                                                               # error_messages argument lets you specify manual error messages for attributes of the field.
                                            "name" : {
                                                "max_length": _("The price must be between 0 and 999.99"),
                                            },
                                        },
                                        max_digits=5, decimal_places=2
                                        )
    discount_price = models.DecimalField(verbose_name=_("Discount Price"),help_text=_("Maximum 999.99"),
                                        error_messages={                                                               # error_messages argument lets you specify manual error messages for attributes of the field.
                                            "name" : {
                                                "max_length": _("The price must be between 0 and 999.99"),
                                            },
                                        },
                                        max_digits=5, decimal_places=2
                                        )
    is_active = models.BooleanField(default=True, verbose_name=_("Product visibility"), help_text=_("Change product visibility"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_absolute_url(self):
        return reverse("store:product_detail",args=[self.slug])

    def __str__(self):
        return self.title

class ProductSpecificationValue(models.Model):
    """it holds each of the products individual specification or bespoken features"""

    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(verbose_name=_("value"),max_length=255, help_text=_("Product specification value (maximum of 255 words)"))

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")

    def __str__(self):
        return self.value

class ProductImage(models.Model):
    """ the product image table"""

    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(verbose_name=_("image"),help_text=_("Upload a product image"),upload_to="images/", default="images/default.png")
    alt_text = models.CharField(verbose_name = _("Alternative text"),help_text=_("Please add alternative text"), max_length=255, null=True, blank=True)
    is_feature = models.BooleanField(default=False)                                                    # we may have multiple images for a particular product so we need to flag one as is featured so the main image so that we can only view rest of the images when we actually view the individual product
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")