from cgi import test
import unittest
from ping.api_resources import payments_api
from ping.payments_api import PaymentsApi
import os
from dotenv import load_dotenv

class testHelper(unittest.TestCase):
    load_dotenv()
    def run_tests(self, response, status = 200):
        self.assertIsNotNone(response)
        if status > 204:
            self.assertEqual(response.status_code, status)
            self.assertFalse(response.is_success())
            self.assertTrue(response.is_error())
            self.assertIsNotNone(response.body)
        else:
            self.assertEqual(response.status_code, status)
            self.assertFalse(response.is_error())
            self.assertTrue(response.is_success())
            self.assertIsNotNone(response.body)
            self.assertIsNone(response.errors)


    def api_is_connected():
        payments_api = PaymentsApi(os.getenv("TENANT_ID"))
        ping = payments_api.ping.ping_the_api()
        return True if ping.body == "pong" else False

        #creates a payment order and a payment to that order that now is ready to get closed, split and settled
    def prepare_payment_order_handling():
        payments_api = PaymentsApi(os.getenv("TENANT_ID"))
        payment_order = payments_api.paymentOrder.create(os.getenv("SPLIT_TREE_ID"), "SEK")
        payment_order_id = payment_order.body["id"]
        payments_api.payment.initiate(testHelper.get_payment_body(), payment_order_id)

        return payment_order_id

    def get_payment_body():
        dummy_body = {
            "currency": "SEK",
            "metadata": {
                "delivery_id": "368745"
                },
            "method": "dummy",
            "order_items": [
                {
                    "amount": 2500,
                    "merchant_id": os.getenv("MERCHANT_ID"),
                    "name": "Delivery, Marios Pasta (Pasta La Vista)",
                    "vat_rate": 12
                },
            ],
            "provider": "dummy",
            "provider_method_parameters": {
                "desired_payment_status": "COMPLETED"
            },
            "total_amount": 2500
        }
        return dummy_body
