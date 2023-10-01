from unittest.mock import Mock, patch

from django.test import TestCase
from model_bakery import baker

from apps.shop.models import Product
from apps.shop.recommender import Recommender


class RecommenderTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.redis_patch = patch('apps.shop.recommender.redis.Redis', Mock())
        cls.redis_patch.start()

    @classmethod
    def tearDownClass(cls):
        cls.redis_patch.stop()
        super().tearDownClass()

    def setUp(self):
        self.recommender = Recommender()

    def test_get_product_key(self):
        product_id = '4a2663f3-c227-47e7-bffe-c68a177e7e38'
        expected_key = 'product:4a2663f3-c227-47e7-bffe-c68a177e7e38:purchased_with'    # noqa
        self.assertEqual(
            self.recommender.get_product_key(product_id), expected_key
        )

    def test_products_bought(self):
        # Create test products using baker
        product1 = baker.make(Product, name='Product 1')
        product2 = baker.make(Product, name='Product 2')

        # Simulate products bought together
        self.recommender.products_bought([product1, product2])

        # Assertions related to the mocked Redis connection
        self.recommender.conn.zincrby.assert_called_with(
            self.recommender.get_product_key(product2.id), 1, str(product1.id),
        )

    def test_suggest_products_for_single_product(self):
        # Create test products using baker
        product1 = baker.make(Product, name='Product 1')
        product2 = baker.make(Product, name='Product 2')

        # Simulate products bought together
        self.recommender.products_bought([product1, product2])

        # Simulate products suggestions
        products = [
            s.encode('utf-8') for s in [str(product1.id), str(product2.id)]
        ]
        self.recommender.conn.zrange.return_value = products
        self.recommender.conn.zrange.reset_mock()

        self.recommender.suggest_products_for([product1])

        # Assertions related to the mocked Redis connection
        self.recommender.conn.zrange.assert_called_once_with(
            self.recommender.get_product_key(product1.id),
            0, -1, desc=True
        )

    def test_suggest_products_for_multiple_products(self):
        # Create test products using baker
        product1 = baker.make(Product, name='Product 1')
        product2 = baker.make(Product, name='Product 2')
        product3 = baker.make(Product, name='Product 3')

        # Simulate products bought together
        self.recommender.products_bought([product1, product2])
        self.recommender.products_bought([product2, product3])

        # Simulate products suggestions
        products = [
            s.encode('utf-8') for s in [str(product1.id), str(product3.id)]
        ]

        self.recommender.conn.zunionstore.return_value = products
        self.recommender.conn.zrange.return_value = products

        self.recommender.suggest_products_for([product1, product3])

        # Assertions related to the mocked Redis connection
        flat_ids = "".join([str(id) for id in [product1.id, product3.id]])
        tmp_key = f"tmp_{flat_ids}"
        self.recommender.conn.zunionstore.assert_called_once()
        self.recommender.conn.zrem.assert_called_once()
        self.recommender.conn.zrange.assert_called_once_with(
            tmp_key, 0, -1, desc=True)
        self.recommender.conn.zrange.reset_mock()

    def test_clear_purchases(self):
        # Create test products using baker
        product1 = baker.make(Product, name='Product 1')
        product2 = baker.make(Product, name='Product 2')

        # Simulate products bought together
        self.recommender.products_bought([product1, product2])

        # Clear purchases
        self.recommender.clear_purchases()

        # Assertions related to the mocked Redis connection
        self.recommender.conn.delete.assert_called()
