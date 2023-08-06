"""Cli product."""

import random
import asyncio

from python_graphql_client import GraphqlClient


from funpinpin_cli.core.util.simple_db import db

from .haikunator_helper import HaikunatorHelper


class Product(object):
    """Product interface."""

    ADMIN_URL = "https://{shop}/admin/internal/web/graphql/core/"
    QUERY = """
        mutation productCreate($product: ProductInput!, $media: [CreateMediaInput!]) {
            productCreate(input: $product, media: $media) {
                product {
                    id
                    title
                    subTitle
                }
                userErrors {
                    field
                    message
                }
            }
        }
    """

    def __init__(self, count=5):
        """Init."""
        self.count = count
        self.shop_token = db.get("shop_token")
        self.shop = db.get("shop")
        if not self.shop_token or not self.shop:
            raise ValueError("please login.")
        self.url = Product.ADMIN_URL.format(shop=self.shop)
        self.client = GraphqlClient(endpoint=self.url)

    def _generate_price(self):
        price = random.uniform(1, 10)
        price = "{:.2f}".format(price)
        return price

    def _generate_title(self):
        h_helper = HaikunatorHelper()
        return h_helper.generate_title()

    def _prepare_h_v(self):
        """Prepare graphql headers and variables."""
        headers = {"Authorization": f"{self.shop_token}"}
        variables = {
            "product": {
                "title": self._generate_title(),
                "status": "ACTIVE",
                "variants": [{"price": self._generate_price()}],
                "vendor": self.shop.split(".v3")[0]
            }
        }
        return headers, variables

    def create_single(self):
        """Create product."""
        headers, variables = self._prepare_h_v()
        data = self.client.execute(
            query=Product.QUERY, variables=variables, headers=headers
        )
        return data

    def run(self):
        """Create products."""
        for i in range(self.count):
            data = self.create_single()
            product = data["data"]["productCreate"]["product"]
            if product:
                yield True, product
            else:
                error_msg = \
                    data["data"]["productCreate"]["userErrors"][0]["message"]
                yield False, error_msg

    async def async_create(self):
        """Async create product."""
        products = []
        for i in range(self.count):
            headers, variables = self._prepare_h_v()
            product = await self.client.execute_async(
                query=Product.QUERY, headers=headers, variables=variables
            )
            products.append(product)
        return products

    def async_run(self):
        """Async create products."""
        loop = asyncio.get_event_loop()
        try:
            products = loop.run_until_complete(self.async_create())
        finally:
            loop.close()
        for data in products:
            product = data["data"]["productCreate"]["product"]
            if product:
                yield True, product
            else:
                error_msg = \
                    data["data"]["productCreate"]["userErrors"][0]["message"]
                yield False, error_msg
