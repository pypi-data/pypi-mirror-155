import unittest
import uuid
import os
from dotenv import load_dotenv
from ping.payments_api import PaymentsApi
from test_helper import testHelper


@unittest.skipUnless(testHelper.api_is_connected(), "A connection to the API is needed")
class TestPayment(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.test_helper = testHelper
        cls.payment_order_id = os.getenv("PAYMENT_ORDER_ID_OPEN")
        cls.payments_api = PaymentsApi(os.getenv("TENANT_ID"))
        cls.dummy_body = cls.test_helper.get_payment_body()

# Get Payments Tests
    # gets payment correctly
    def test_get_payment_200(self):
        payment_id = os.getenv("PAYMENT_ID")

        response = self.payments_api.payment.get(self.payment_order_id, payment_id)
        self.test_helper.run_tests(self, response, 200)

    # gets payment with an incorrect id
    def test_get_payment_404(self):
        payment_id = ""

        response = self.payments_api.payment.get(self.payment_order_id, payment_id)
        self.test_helper.run_tests(self, response, 404)

# Initiate Payment Tests
    # Initiate a correct payment (status code 200)
    def test_initiate_payment_200(self):
        response = self.payments_api.payment.initiate(self.dummy_body, self.payment_order_id)
        self.test_helper.run_tests(self, response)

    # Initiate a payment with incorrect values inside payment object (status code 422)
    def test_initiate_payment_422(self):
        payment_order_id = 0
        self.dummy_body["method"] = 0

        response = self.payments_api.payment.initiate(self.dummy_body, payment_order_id)
        self.test_helper.run_tests(self, response, 422)

    # Initiate a payment on a non-existing payment order (status code 404)
    def test_initiate_payment_404(self):
        error_payment_order_id = uuid.uuid4()

        response = self.payments_api.payment.initiate(self.dummy_body, error_payment_order_id)
        self.test_helper.run_tests(self, response, 404)


if __name__ == '__main__':
    unittest.main()
