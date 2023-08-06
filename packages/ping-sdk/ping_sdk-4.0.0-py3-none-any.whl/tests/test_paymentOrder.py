import unittest
import uuid
import os
from dotenv import load_dotenv
from ping.payments_api import PaymentsApi
from test_helper import testHelper


@unittest.skipUnless(testHelper.api_is_connected(), "A connection to the API is needed")
class TestPaymentOrder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.payments_api = PaymentsApi(os.getenv("TENANT_ID"))
        cls.split_tree_id = os.getenv("SPLIT_TREE_ID")
        cls.test_helper = testHelper

    def setUp(self):
        self.payment_order_id = os.getenv("PAYMENT_ORDER_ID")

# Get Payment Orders Tests
    # get payment orders correctly (status code 200)
    def test_list_200(self): 
    
        response_date = self.payments_api.paymentOrder.list("2020-03-27T09:42:30Z", "2022-03-27T09:42:30Z")
        response = self.payments_api.paymentOrder.list()

        # tests with start-end date
        self.test_helper.run_tests(self, response_date)

        # tests without date
        self.test_helper.run_tests(self, response)

    # get payment orders with impossible dates (status code 422)
    def test_list_422(self):
        response_date = self.payments_api.paymentOrder.list("12/90/2019", "40/10/2020")
        self.test_helper.run_tests(self, response_date, 422)

# Create Payment Order Tests
    # creates a payment order correctly (status code 200)
    def test_create_200(self):
        response = self.payments_api.paymentOrder.create(self.split_tree_id, "SEK")
        self.test_helper.run_tests(self, response)

    # creates a payment orders with incorrect id format (status code 422)
    def test_create_422(self):
        response = self.payments_api.paymentOrder.create(self.split_tree_id, "")
        self.test_helper.run_tests(self, response, 422)

# Get Payment Order Tests
    # gets a payment order correctly (status code 200)
    def test_get_200(self):
        response = self.payments_api.paymentOrder.get(self.payment_order_id)
        self.test_helper.run_tests(self, response)
    
    # get a payment order with incorrect id format (status code 422)
    def test_get_422(self):
        response = self.payments_api.paymentOrder.get(0)
        self.test_helper.run_tests(self, response, 422)
    
    # get a payment order with a non-existing id (status code 404)
    def test_get_404(self):
        response = self.payments_api.paymentOrder.get(uuid.uuid4())
        self.test_helper.run_tests(self, response, 404)

# Update Payment Order Tests
    # updates a payment order correctly (status code 204)
    def test_update_204(self):
        
        response = self.payments_api.paymentOrder.update(
            os.getenv("PAYMENT_ORDER_ID_OPEN"),
            self.split_tree_id
        )
        self.test_helper.run_tests(self, response, 204)
        

    # updates a payment order with incorrect id format (status code 422)
    def test_update_422(self):
        
        response = self.payments_api.paymentOrder.update(
            0,
            self.split_tree_id
        )
        self.test_helper.run_tests(self, response, 422)
        

    # updates a payment order with a non-existing id (status code 404)
    def test_update_404(self):
        
        response = self.payments_api.paymentOrder.update(
            "",
            self.split_tree_id
        )
        self.test_helper.run_tests(self, response, 404)
        

# Close Payment Order Tests
    # closes a payment order correctly (status code 204)
    def test_close_204(self):
        response = self.payments_api.paymentOrder.close(self.payment_order_id)
        self.test_helper.run_tests(self, response, 204)

    # closes a payment order with an incorrect id format (status code 422)
    def test_close_422(self):
        response = self.payments_api.paymentOrder.close(0)
        self.test_helper.run_tests(self, response, 422)

    # closes a payment order with a non-existing id (status code 404)
    def test_close_404(self):
        response = self.payments_api.paymentOrder.close(uuid.uuid4())
        self.test_helper.run_tests(self, response, 404)

# Split Payment Order Tests
    # splits a payment order correctly (status code 204)
    def test_split_204(self):
        response = self.payments_api.paymentOrder.split(self.payment_order_id)
        self.test_helper.run_tests(self, response, 204)

    # fast forwards and splits a payment order correctly (status code 204)
    def test_split_fast_forward_204(self):
        payment_order_id = self.test_helper.prepare_payment_order_handling()
        response = self.payments_api.paymentOrder.split(payment_order_id, fast_forward=True)
        self.test_helper.run_tests(self, response, 204)

    # splits a payment order with an incorrect id format (status code 422)
    def test_split_422(self):
        response = self.payments_api.paymentOrder.split(0)
        self.test_helper.run_tests(self, response, 422)

    # splits a payment order with a non-existing id (status code 404)
    def test_split_404(self):
        response = self.payments_api.paymentOrder.split(uuid.uuid4())
        self.test_helper.run_tests(self, response, 404)

# Settle Payment Order Tests
    # settles a payment correctly (status code 204)
    def  test_settle_204(self):
        response = self.payments_api.paymentOrder.settle(self.payment_order_id)
        self.test_helper.run_tests(self, response, 204)
    
    # fast forwards and settles a payment correctly (status code 204)
    def  test_settle_order_fast_forward_204(self):
        payment_order_id = self.test_helper.prepare_payment_order_handling()
        response = self.payments_api.paymentOrder.settle(payment_order_id, fast_forward=True)
        self.test_helper.run_tests(self, response, 204)

    # settles a payment with an incorrect id format (status code 422)
    def  test_settle_422(self):
        response = self.payments_api.paymentOrder.settle(0)
        self.test_helper.run_tests(self, response, 422)

    # settles a payment with a non-existing id (status code 404)
    def  test_settle_404(self):
        response = self.payments_api.paymentOrder.settle(uuid.uuid4())
        self.test_helper.run_tests(self, response, 404)


if __name__ == '__main__':
    unittest.main()
