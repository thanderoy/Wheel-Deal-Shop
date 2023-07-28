from django.db import models
from django.urls import reverse
from apps.common.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"])
        ]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_cat_list", args=[self.slug])


class Product(BaseModel):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(
        upload_to="products/%Y/%m/%d", blank=True
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)    # Avoid FloatField due to rounding issues.
    available =  models.BooleanField(default=True)
    
    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]
        
    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])
    
