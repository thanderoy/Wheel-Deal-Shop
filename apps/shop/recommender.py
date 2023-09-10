import redis
from django.conf import settings

from .models import Product


class Recommender:
    """
    Stores product purchases and retrieve product suggestions for a given
        product or products.
    """
    def __init__(self):
        self.conn = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            # username=settings.REDIS_USERNAME,
            # password=settings.REDIS.PASSWORD
        )

    def get_product_key(self, id: str):
        """
        Given a product ID, builds the Redis key for the sorted set with
            related product.

        params:id (uuid): Product ID

        return:(str): Products's Redis key -> product:[id]:purchased_with
        """
        return f"product:{str(id)}:purchased_with"

    def products_bought(self, products):
        """
        Given a list of Product objects that have been bought together.
            (in the same Order object).
            *-> [orderitem.product for orderitem in order.items.all()]
         * For each product_id, get other products bought with it
         * Get the product's Redis key using get_product_id()
         * Increment score of each product_id in the sorted set

        params:products (list): List of Product objects
        """
        product_ids = [str(p.id) for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # Get other products bought with each product
                if product_id != with_id:
                    self.conn.zincrby(
                        self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products: list, max_results=6):
        """
        Given a list of Product objects,
            - If one product given, use ZRANGE to get IDs of products bought
                together ordered by frequency of being bought together.
            - If multiple products given, store them in a temporary Redis key,
                -> use ZUNIONSTORE to create a sorted set with the given keys
                as well as the aggreggated sum of scores of the elememnts in
                the new Redis key.
                -> use ZREM to remove the product we are generating suggestions
                for.
                -> use ZRANGE as above.
            - Finally, get Product objects using IDs

        !IMPORTANT - IDs on this project use uuid4s, so yeah...should be fun :)

        :params products (list): Product objects to get suggestions for.
        :params max_results (int, optional): Maximum suggestions. Defaults to 6.

        :return (list): Suggested Products objects
        """
        product_ids = [str(p.id) for p in products]
        if len(products) == 1:
            # One product only
            suggestions = self.conn.zrange(
                self.get_product_key(product_ids[0]),
                0, -1, desc=True
            )[:max_results]
        else:   # Multiple products
            # Generate temporary key
            flat_ids = "".join([str(id) for id in product_ids])
            tmp_key = f"tmp_{flat_ids}"

            # Combine scores of all products and store
            #   resulting sorted set in temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            self.conn.zunionstore(tmp_key, keys)

            # Remove IDs for the product we are generating suggestions for
            self.conn.zrem(tmp_key, *product_ids)

            # Get the product IDs with their score, descending order
            suggestions = self.conn.zrange(
                tmp_key, 0, -1, desc=True)[:max_results]

            # Remove the temporary key
            self.conn.delete(tmp_key)
        suggested_products_ids = [id.decode('utf-8') for id in suggestions]

        # Get suggested products and sort by order of appearance
        suggested_products = list(Product.objects.filter(
            id__in=suggested_products_ids
        ))
        suggested_products.sort(
            key=lambda x: suggested_products_ids.index(str(x.id))
        )
        return suggested_products

    def clear_purchases(self):
        """
        Clear recommendations.
        """
        products = Product.objects.values_list('id', flat=True)
        for id in products.iterator():
            self.conn.delete(self.get_product_key(id))
