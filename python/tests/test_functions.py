import unittest
import stripe
from unittest import mock
from stripe_agent_toolkit.functions import (
    create_customer,
    list_customers,
    create_product,
    list_products,
    create_price,
    list_prices,
    create_payment_link,
    create_invoice,
    create_invoice_item,
    finalize_invoice,
    retrieve_balance,
)


class TestStripeFunctions(unittest.TestCase):
    def test_create_customer(self):
        with mock.patch("stripe.Customer.create") as mock_function:
            mock_customer = {"id": "cus_123"}
            mock_function.return_value = stripe.Customer.construct_from(
                mock_customer, "sk_test_123"
            )

            result = create_customer(
                name="Test User", email="test@example.com"
            )

            self.assertEqual(result, {"id": mock_customer["id"]})

    def test_list_customers(self):
        with mock.patch("stripe.Customer.list") as mock_function:
            mock_customers = [{"id": "cus_123"}, {"id": "cus_456"}]

            mock_function.return_value = stripe.ListObject.construct_from(
                {
                    "object": "list",
                    "data": [
                        stripe.Customer.construct_from(
                            {
                                "id": "cus_123",
                                "email": "customer1@example.com",
                                "name": "Customer One",
                            },
                            "sk_test_123",
                        ),
                        stripe.Customer.construct_from(
                            {
                                "id": "cus_456",
                                "email": "customer2@example.com",
                                "name": "Customer Two",
                            },
                            "sk_test_123",
                        ),
                    ],
                    "has_more": False,
                    "url": "/v1/customers",
                },
                "sk_test_123",
            )

            result = list_customers()
            self.assertEqual(result, mock_customers)

    def test_create_product(self):
        with mock.patch("stripe.Product.create") as mock_function:
            mock_product = {"id": "prod_123"}
            mock_function.return_value = stripe.Product.construct_from(
                mock_product, "sk_test_123"
            )

            result = create_product(name="Test Product")

            self.assertEqual(result, {"id": mock_product["id"]})

    def test_list_products(self):
        with mock.patch("stripe.Product.list") as mock_function:
            mock_products = [
                {"id": "prod_123", "name": "Product One"},
                {"id": "prod_456", "name": "Product Two"},
            ]

            mock_function.return_value = stripe.ListObject.construct_from(
                {
                    "object": "list",
                    "data": [
                        stripe.Product.construct_from(
                            {
                                "id": "prod_123",
                                "name": "Product One",
                            },
                            "sk_test_123",
                        ),
                        stripe.Product.construct_from(
                            {
                                "id": "prod_456",
                                "name": "Product Two",
                            },
                            "sk_test_123",
                        ),
                    ],
                    "has_more": False,
                    "url": "/v1/products",
                },
                "sk_test_123",
            )

            result = list_products()
            self.assertEqual(result, mock_products)

    def test_create_price(self):
        with mock.patch("stripe.Price.create") as mock_function:
            mock_price = {"id": "price_123"}
            mock_function.return_value = stripe.Price.construct_from(
                mock_price, "sk_test_123"
            )

            result = create_price(
                product="prod_123", currency="usd", unit_amount=1000
            )

            self.assertEqual(result, {"id": mock_price["id"]})

    def test_list_prices(self):
        with mock.patch("stripe.Price.list") as mock_function:
            mock_prices = [
                {"id": "price_123", "product": "prod_123"},
                {"id": "price_456", "product": "prod_456"},
            ]

            mock_function.return_value = stripe.ListObject.construct_from(
                {
                    "object": "list",
                    "data": [
                        stripe.Price.construct_from(
                            {
                                "id": "price_123",
                                "product": "prod_123",
                            },
                            "sk_test_123",
                        ),
                        stripe.Price.construct_from(
                            {
                                "id": "price_456",
                                "product": "prod_456",
                            },
                            "sk_test_123",
                        ),
                    ],
                    "has_more": False,
                    "url": "/v1/prices",
                },
                "sk_test_123",
            )

            result = list_prices()

            self.assertEqual(result, mock_prices)

    def test_create_payment_link(self):
        with mock.patch("stripe.PaymentLink.create") as mock_function:
            mock_payment_link = {"id": "pl_123", "url": "https://example.com"}
            mock_function.return_value = stripe.PaymentLink.construct_from(
                mock_payment_link, "sk_test_123"
            )

            result = create_payment_link(price="price_123", quantity=1)

            self.assertEqual(result, mock_payment_link)

    def test_create_invoice(self):
        with mock.patch("stripe.Invoice.create") as mock_function:
            mock_invoice = {
                "id": "in_123",
                "hosted_invoice_url": "https://example.com",
                "customer": "cus_123",
                "status": "open",
            }

            mock_function.return_value = stripe.Invoice.construct_from(
                mock_invoice, "sk_test_123"
            )

            result = create_invoice(customer="cus_123")

            self.assertEqual(
                result,
                {
                    "id": mock_invoice["id"],
                    "hosted_invoice_url": mock_invoice["hosted_invoice_url"],
                    "customer": mock_invoice["customer"],
                    "status": mock_invoice["status"],
                },
            )

    def test_create_invoice_item(self):
        with mock.patch("stripe.InvoiceItem.create") as mock_function:
            mock_invoice_item = {"id": "ii_123", "invoice": "in_123"}
            mock_function.return_value = stripe.InvoiceItem.construct_from(
                mock_invoice_item, "sk_test_123"
            )

            result = create_invoice_item(
                customer="cus_123", price="price_123", invoice="in_123"
            )

            self.assertEqual(
                result,
                {
                    "id": mock_invoice_item["id"],
                    "invoice": mock_invoice_item["invoice"],
                },
            )

    def test_finalize_invoice(self):
        with mock.patch("stripe.Invoice.finalize_invoice") as mock_function:
            mock_invoice = {
                "id": "in_123",
                "hosted_invoice_url": "https://example.com",
                "customer": "cus_123",
                "status": "open",
            }

            mock_function.return_value = stripe.Invoice.construct_from(
                mock_invoice, "sk_test_123"
            )

            result = finalize_invoice(invoice="in_123")

            self.assertEqual(
                result,
                {
                    "id": mock_invoice["id"],
                    "hosted_invoice_url": mock_invoice["hosted_invoice_url"],
                    "customer": mock_invoice["customer"],
                    "status": mock_invoice["status"],
                },
            )

    def test_retrieve_balance(self):
        with mock.patch("stripe.Balance.retrieve") as mock_function:
            mock_balance = {"available": [{"amount": 1000, "currency": "usd"}]}

            mock_function.return_value = stripe.Balance.construct_from(
                mock_balance, "sk_test_123"
            )

            result = retrieve_balance()

            self.assertEqual(result, mock_balance)


if __name__ == "__main__":
    unittest.main()
