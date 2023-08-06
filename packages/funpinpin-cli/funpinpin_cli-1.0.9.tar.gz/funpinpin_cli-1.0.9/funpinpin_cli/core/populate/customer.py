"""Cli customer."""

import asyncio

from python_graphql_client import GraphqlClient

from funpinpin_cli.core.util.simple_db import db

from .haikunator_helper import HaikunatorHelper


class Customer(object):
    """Customer interface."""

    ADMIN_URL = "https://{shop}/admin/internal/web/graphql/core/"
    QUERY = """
        mutation consumerCreate($input: ConsumerInput!) {
            consumerCreate(input: $input) {
                consumer {
                    id
                    email
                    firstName
                    lastName
                }
                userErrors {
                    field
                    message
                    code
                }
                __typename
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
        self.url = Customer.ADMIN_URL.format(shop=self.shop)
        self.client = GraphqlClient(endpoint=self.url)

    def _generate_name(self):
        h_helper = HaikunatorHelper()
        return h_helper.generate_name()

    def _generate_email(self):
        h_helper = HaikunatorHelper()
        return h_helper.generate_email()

    def _prepare_h_v(self):
        headers = {"Authorization": f"{self.shop_token}"}
        first_name, last_name = self._generate_name()
        variables = {
            "input": {
                "email": self._generate_email(),
                "firstName": first_name,
                "lastName": last_name
             }
        }
        return headers, variables

    def create_single(self):
        """Create single customer."""
        headers, variables = self._prepare_h_v()
        data = self.client.execute(
            query=Customer.QUERY, variables=variables, headers=headers
        )
        return data

    def run(self):
        """Create customers."""
        for i in range(self.count):
            data = self.create_single()
            customer = data["data"]["consumerCreate"]["consumer"]
            if customer:
                yield True, customer
            else:
                error_msg = \
                    data["data"]["consumerCreate"]["userErrors"][0]["message"]
                yield False, error_msg

    async def async_create(self):
        """Async create customer."""
        customers = []
        for i in range(self.count):
            headers, variables = self._prepare_h_v()
            customer = await self.client.execute_async(
                query=Customer.QUERY, headers=headers, variables=variables
            )
            customers.append(customer)
        return customers

    def async_run(self):
        """Async create customers."""
        loop = asyncio.get_event_loop()
        try:
            customers = loop.run_until_complete(self.async_create())
        finally:
            loop.close()
        for data in customers:
            customer = data["data"]["consumerCreate"]["consumer"]
            if customer:
                yield True, customer
            else:
                error_msg = \
                    data["data"]["consumerCreate"]["userErrors"][0]["message"]
                yield False, error_msg
