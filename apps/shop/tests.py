import datetime
import uuid

import pytest
import pytz
from django.test import TestCase

from apps.shop.models import Category, Product


class TestCategory:
    def test_create_category_with_valid_name_and_slug(self):
        category = Category(name='Test Category', slug='test-category')
        category.save()
        assert Category.objects.filter(
            name='Test Category', slug='test-category'
        ).exists()

    def test_save_category_with_valid_name_and_slug(self):
        category = Category(name='Test Category', slug='test-category')
        category.save()
        category.name = 'Updated Category'
        category.save()
        assert Category.objects.filter(
            name='Updated Category', slug='test-category'
        ).exists()

    def test_retrieve_category_by_name_or_slug(self):
        category = Category(name='Test Category', slug='test-category')
        category.save()
        retrieved_by_name = Category.objects.get(name='Test Category')
        retrieved_by_slug = Category.objects.get(slug='test-category')
        assert retrieved_by_name == retrieved_by_slug

    def test_create_category_with_empty_name(self):
        with pytest.raises(Exception):
            category = Category(name='', slug='test-category')
            category.save()

    def test_create_category_with_name_exceeding_max_length(self):
        with pytest.raises(Exception):
            category = Category(
                name='This is a very long category name that exceeds \
                    the maximum length allowed',
                slug='test-category'
            )
            category.save()

    def test_create_category_with_non_unique_slug(self):
        category1 = Category(name='Category 1', slug='test-category')
        category1.save()
        with pytest.raises(Exception):
            category2 = Category(name='Category 2', slug='test-category')
            category2.save()

    def test_retrieve_nonexistent_category(self):
        category_name = 'Nonexistent Category'
        category_slug = 'nonexistent-category'
        category = Category.objects.filter(name=category_name).first()
        assert category is None

        category = Category.objects.filter(slug=category_slug).first()
        assert category is None

    def test_retrieve_categories_ordered_by_creation_date(self):
        # Create Category instances
        category1 = Category.objects.create(name='Cat 1', slug='cat-1')
        category2 = Category.objects.create(name='Cat 2', slug='cat-2')
        category3 = Category.objects.create(name='Cat 3', slug='cat-3')

        # Retrieve all Category instances ordered by creation date
        categories = Category.objects.order_by('-created')

        # Check if the retrieved categories are in the correct order
        self.assertEqual(categories[0], category3)
        self.assertEqual(categories[1], category2)
        self.assertEqual(categories[2], category1)


class TestProduct(TestCase):
    def test_create_product_with_all_fields(self):
        category = Category.objects.create(name='Test Cat', slug='test-cat')
        product = Product.objects.create(
            category=category, name='Test Product', slug='test-product',
            price=10.99
        )
        assert product.name == 'Test Product'
        assert product.slug == 'test-product'
        assert product.price == 10.99

    def test_update_existing_product(self):
        category = Category.objects.create(name='Test Cat', slug='test-cat')
        product = Product.objects.create(
            category=category, name='Test Product', slug='test-product',
            price=10.99
        )
        product.name = 'Updated Product'
        product.save()
        updated_product = Product.objects.get(id=product.id)
        assert updated_product.name == 'Updated Product'

    def test_retrieve_product_by_id(self):
        category = Category.objects.create(name='Test Cat', slug='test-cat')
        product = Product.objects.create(
            category=category, name='Test Product', slug='test-product',
            price=10.99
        )
        retrieved_product = Product.objects.get(id=product.id)
        assert retrieved_product.name == 'Test Product'

    def test_retrieve_product_by_slug(self):
        category = Category.objects.create(name='Test Cat', slug='test-cat')
        product = Product.objects.create(
            category=category, name='Test Product', slug='test-product',
            price=10.99
        )
        retrieved_product = Product.objects.get(slug='test-product')
        assert retrieved_product.name == product.name

    def test_create_product_with_non_unique_slug(self):
        category = Category.objects.create(name='Test Cat', slug='test-cat')
        Product.objects.create(
            category=category, name='Test Product', slug='test-product',
            price=10.99
        )
        assert Product.objects.get(name='test-product').exists() is True
        with pytest.raises(Product.IntegrityError):
            Product.objects.create(
                category=category, name='Test Product', slug='test-product',
                price=10.99
            )

    def test_create_product_with_negative_price(self):
        category = Category.objects.create(name='Test Cat', slug='test-cat')
        with pytest.raises(Product.ValidationError):
            Product.objects.create(
                category=category, name='Test Product', slug='test-product',
                price=-10.99
            )

    def test_retrieving_nonexistent_product_by_id(self):
        product_id = uuid.uuid4()
        product = Product.objects.filter(id=product_id).first()
        assert product is None

    def test_retrieving_nonexistent_product_by_slug(self):
        slug = 'nonexistent-slug'
        product = Product.objects.filter(slug=slug).first()
        assert product is None

    def test_delete_product(self):
        category = Category.objects.create(name='Test Cat', slug='test-cat')
        product = Product.objects.create(
            category=category, name='Test Product', slug='test-product',
            price=10.99
        )
        product_id = product.id
        product.delete()
        with pytest.raises(Product.DoesNotExist):
            Product.objects.get(id=product_id)

    def test_retrieve_products_in_category(self):
        category = Category.objects.create(name='Test Cat', slug='test-cat')
        product1 = Product.objects.create(
            category=category, name='Product 1', slug='product-1',
            price=10.99
        )
        product2 = Product.objects.create(
            category=category, name='Product 2', slug='product-2',
            price=10.99
        )
        products = category.products.all()
        assert len(products) == 2
        assert product1 in products
        assert product2 in products

    def test_retrieving_all_available_products(self):
        # Create test data
        category = Category.objects.create(name='Test Cat', slug='test-cat')
        product1 = Product.objects.create(category=category, name='Product 1', slug='product-1', price=10.00, available=True)
        product2 = Product.objects.create(category=category, name='Product 2', slug='product-2', price=20.00, available=True)
        product3 = Product.objects.create(category=category, name='Product 3', slug='product-3', price=30.00, available=False)
        # Retrieve all available products
        available_products = Product.objects.filter(available=True)

        # Assert that only the available products are retrieved
        assert len(available_products) == 2
        assert product1 in available_products
        assert product2 in available_products
        assert product3 not in available_products

    # Tests that all products created after a certain date are retrieved
    def test_retrieve_products_created_after_date(self):
        # Create a category
        category = Category.objects.create(name='Test Cat', slug='test-cat')
        # Create products with different creation dates
        product1 = Product.objects.create(category=category, name='Product 1', slug='product-1', price=10.00)
        product2 = Product.objects.create(category=category, name='Product 2', slug='product-2', price=20.00)
        product3 = Product.objects.create(category=category, name='Product 3', slug='product-3', price=30.00)
        # Set a certain date
        certain_date = datetime.datetime(2022, 1, 1, tzinfo=pytz.UTC)
        # Retrieve products created after the certain date
        products = Product.objects.filter(created__gt=certain_date)
        # Assert that the correct products are retrieved
        assert product2 in products
        assert product3 in products
        assert product1 not in products
