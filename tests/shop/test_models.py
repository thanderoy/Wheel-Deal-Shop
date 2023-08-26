import uuid

import pytest
from django.test import TestCase
from model_bakery import baker

from apps.shop.models import Category, Product


class CategoryTestCase(TestCase):

    def test_create_category_with_valid_name_and_slug(self):
        baker.make(Category, name='Test Category', slug='test-category')
        assert Category.objects.filter(
            name='Test Category', slug='test-category'
        ).exists()

    def test_save_category_with_valid_name_and_slug(self):
        category = baker.make(Category, name='Test Category', slug='test-category') # noqa
        category.name = 'Updated Category'
        category.save()
        assert Category.objects.filter(
            name='Updated Category', slug='test-category'
        ).exists()

    def test_retrieve_category_by_name_or_slug(self):
        baker.make(Category, name='Test Category', slug='test-category')
        retrieved_by_name = Category.objects.get(name='Test Category')
        retrieved_by_slug = Category.objects.get(slug='test-category')
        assert retrieved_by_name == retrieved_by_slug

    def test_create_category_with_non_unique_slug(self):
        baker.make(Category, name='Category 1', slug='test-category')
        with pytest.raises(Exception):
            baker.make(Category, name='Category 2', slug='test-category')

    def test_retrieve_nonexistent_category(self):
        category_name = 'Nonexistent Category'
        category_slug = 'nonexistent-category'
        category = Category.objects.filter(name=category_name).first()
        assert category is None

        category = Category.objects.filter(slug=category_slug).first()
        assert category is None

    def test_retrieve_categories_ordered_by_creation_date(self):
        # Create Category instances using baker.make
        category1 = baker.make(Category, name='Cat 1', slug='cat-1')
        category2 = baker.make(Category, name='Cat 2', slug='cat-2')
        category3 = baker.make(Category, name='Cat 3', slug='cat-3')

        # Retrieve all Category instances ordered by creation date
        categories = Category.objects.order_by('-created')

        # Check if the retrieved categories are in the correct order
        self.assertEqual(categories[0], category3)
        self.assertEqual(categories[1], category2)
        self.assertEqual(categories[2], category1)


class ProductTestCase(TestCase):
    def test_create_product_with_all_fields(self):
        category = baker.make(Category, name='Test Cat', slug='test-cat')
        product = baker.make(
            Product, category=category, name='Test Product',
            slug='test-product', price=10.99
        )
        assert product.name == 'Test Product'
        assert product.slug == 'test-product'
        assert product.price == 10.99

    def test_update_existing_product(self):
        category = baker.make(Category, name='Test Cat', slug='test-cat')
        product = baker.make(
            Product, category=category, name='Test Product',
            slug='test-product', price=10.99
        )
        product.name = 'Updated Product'
        product.save()
        updated_product = Product.objects.get(id=product.id)
        assert updated_product.name == 'Updated Product'

    def test_retrieve_product_by_id(self):
        category = baker.make(Category, name='Test Cat', slug='test-cat')
        product = baker.make(
            Product, category=category, name='Test Product',
            slug='test-product', price=10.99
        )
        retrieved_product = Product.objects.get(id=product.id)
        assert retrieved_product.name == 'Test Product'

    def test_retrieve_product_by_slug(self):
        category = baker.make(Category, name='Test Cat', slug='test-cat')
        product = baker.make(
            Product, category=category, name='Test Product',
            slug='test-product', price=10.99
        )
        retrieved_product = Product.objects.get(slug='test-product')
        assert retrieved_product.name == product.name

    def test_create_product_with_non_unique_slug(self):
        category = baker.make(Category, name='Test Cat', slug='test-cat')
        baker.make(
            Product, category=category, name='Test Product',
            slug='test-product', price=10.99
        )

        assert Product.objects.filter(slug='test-product').exists() is True
        with pytest.raises(Exception):
            baker.make(
                Product, category=category, name='Test Product 2',
                slug='test-product', price=10.99
            )

    def test_retrieving_nonexistent_product_by_id(self):
        product_id = uuid.uuid4()
        product = Product.objects.filter(id=product_id).first()
        assert product is None

    def test_retrieving_nonexistent_product_by_slug(self):
        slug = 'nonexistent-slug'
        product = Product.objects.filter(slug=slug).first()
        assert product is None

    def test_retrieve_products_in_category(self):
        category = baker.make(Category, name='Test Cat', slug='test-cat')
        product1 = baker.make(
            Product, category=category, name='Product 1', slug='product-1',
            price=10.99
        )
        product2 = baker.make(
            Product, category=category, name='Product 2', slug='product-2',
            price=10.99
        )
        products = category.products.all()
        assert len(products) == 2
        assert product1 in products
        assert product2 in products

    def test_retrieving_all_available_products(self):
        category = baker.make(Category, name='Test Cat', slug='test-cat')
        product1 = baker.make(
            Product, category=category, name='Product 1', slug='product-1',
            price=10.00, available=True
        )
        product2 = baker.make(
            Product, category=category, name='Product 2', slug='product-2',
            price=20.00, available=True
        )
        product3 = baker.make(
            Product, category=category, name='Product 3', slug='product-3',
            price=30.00, available=False
        )

        available_products = Product.objects.filter(available=True)

        # Assert that only the available products are retrieved
        assert len(available_products) == 2
        assert product1 in available_products
        assert product2 in available_products
        assert product3 not in available_products
