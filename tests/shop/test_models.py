import uuid
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from model_bakery import baker

from apps.shop.models import Category, Product


class TestProduct(TestCase):

    # Tests that a product can be created with all required fields
    def test_create_product_with_required_fields(self):
        category = baker.make(Category, name='Test Cat', slug='test-cat')
        product = baker.make(
            Product, category=category, name='Test Product',
            slug='test-product', price=10.99
        )
        assert product.name == 'Test Product'
        assert product.slug == 'test-product'
        assert product.price == 10.99

    # Tests that a product can be created with optional fields
    def test_create_product_with_optional_fields(self):
        category = baker.make(Category, name='Test Cat', slug='test-cat')
        product = baker.make(
            Product, category=category, name='Test Product',
            slug='test-product', description='Test Description',
            image='test_image.jpg', price=10.99, available=True
        )
        assert product.name == 'Test Product'
        assert product.slug == 'test-product'
        assert product.description == 'Test Description'
        assert product.image == 'test_image.jpg'
        assert product.price == 10.99
        assert product.available is True

    # Tests that a product can be updated
    def test_update_product(self):
        category = baker.make(Category, name='Test Cat', slug='test-cat')
        product = baker.make(
            Product, id=uuid.UUID('4a2663f3-c227-47e7-bffe-c68a177e7e38'),
            category=category, name='Test Product',
            slug='test-product', price=10.99
        )
        product.name = 'Updated Product'
        product.save()
        updated_product = Product.objects.get(
            id='4a2663f3-c227-47e7-bffe-c68a177e7e38'
        )
        assert updated_product == product

    # Tests that a product can be retrieved
    def test_retrieve_product(self):
        category = baker.make(Category, name='Test Cat', slug='test-cat')
        product = baker.make(
            Product, category=category, name='Test Product',
            slug='test-product', price=Decimal(10.99)
        )
        retrieved_product = Product.objects.get(id=product.id)
        assert retrieved_product == product

    # Tests that a product cannot be created with a price value of 0
    def test_create_product_with_zero_price(self):
        category = baker.make(Category, name='Test Cat', slug='test-cat')
        product = baker.make(
            Product, category=category, name='Test Product',
            slug='test-product'
        )
        product.price = Decimal(0.00)
        msg = "Price [0], must be greater than zero(0)"
        with self.assertRaisesMessage(ValidationError, msg):
            product.save()

    # Test that a product cannot be created with a negative price value
    def test_create_product_with_negative_price(self):
        category = baker.make(Category, name='Test Cat', slug='test-cat')
        msg = "Price [-10], must be greater than zero(0)"
        with self.assertRaisesMessage(ValidationError, msg):
            baker.make(
                Product, name='Test Product', slug='test-product',
                description='This is a test product.',
                category=category, price=Decimal(-10.00), available=True
            )

    # Tests that a product cannot be created with a non-numeric price value
    def test_create_product_with_non_numeric_price(self):
        category = baker.make(Category, name='Test Cat', slug='test-cat')
        with self.assertRaises(Exception):
            baker.make(
                Product, category=category, name='Test Product',
                slug='test-product', price='non-numeric'
            )

    # Tests that the method returns a valid URL.
    def test_valid_url_with_name_and_slug(self):
        product = baker.make(
            Product, id=uuid.UUID('4a2663f3-c227-47e7-bffe-c68a177e7e38'),
            name="Test Product", slug="test-product"
        )
        url = product.get_absolute_url()
        assert url == "/en/4a2663f3-c227-47e7-bffe-c68a177e7e38/test-product/"


class TestCategory(TestCase):

    # Tests that a Category object can be created with required fields
    def test_category_creation(self):
        category = baker.make(Category, name="Test Category")
        assert isinstance(category, Category)
        assert category.name == "Test Category"
        assert category.slug is not None

    # Tests that a Category object can be translated to different languages
    def test_category_translation(self):
        category = baker.make(Category)
        translation = category.translations.create(language_code='fr', name='French Category', slug='french-category')
        assert translation.name == 'French Category'
        assert translation.slug == 'french-category'

    # Tests that a Category object's slug must be unique
    def test_category_unique_slug(self):
        baker.make(Category, name='Unique Slug', slug='unique-slug')
        with pytest.raises(IntegrityError):
            baker.make(Category, name='Unique Slug', slug='unique-slug')
