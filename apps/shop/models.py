from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields

from apps.common.models import BaseModel


class Category(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=150, null=False),
        slug=models.SlugField(max_length=150, unique=True),
    )

    class Meta:
        # ordering = ["name"]
        # indexes = [
        #     models.Index(fields=["name"])
        # ]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_cat_list", args=[self.slug])


class Product(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=200),
        slug=models.SlugField(max_length=200),
        description=models.TextField(blank=True),
    )
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    # Avoid FloatField due to rounding issues.
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[
        MinValueValidator(1)
    ])
    available = models.BooleanField(default=True)

    class Meta:
        # ordering = ["name"]
        indexes = [
            # models.Index(fields=["id", "slug"]),
            # models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])

    def validate_non_negative_and_zero_price_values(self):
        if self.price <= 0.00:
            raise ValidationError({
                "price": ["Price [{}], must be greater than zero(0)".format(str(self.price))],     # noqa
            })

    def clean(self):
        super().clean()
        self.validate_non_negative_and_zero_price_values()

    def save(self):
        super().save()
        self.clean()
