import os
import unittest
import uuid
from dotenv import load_dotenv
from ping.payments_api import PaymentsApi
from test_helper import testHelper


@unittest.skipUnless(testHelper.api_is_connected(), "A connection to the API is needed")
class TestMerchant(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()

        cls.payments_api = PaymentsApi(os.getenv("TENANT_ID"))
        cls.test_helper = testHelper

# Get Merchants Tests
    # gets merchants successfully
    def test_list_200(self):
        response = self.payments_api.merchant.list()
        self.test_helper.run_tests(self, response)

# Create New Merchant Tests
    # creates a merchant correctly (status code 200)
    def test_create_200(self):
        response = self.payments_api.merchant.create(
            {
                "name": "Company inc",
                "organization": {
                    "country": "SE",
                    "se_organization_number": "5555555555"
                }
            }
        )
        self.test_helper.run_tests(self, response)
    
    # creates a merchant with incorrect values inside merchant object (status code 422)
    def test_create_422(self):
        response = self.payments_api.merchant.create({})
        self.test_helper.run_tests(self, response, 422)

# Get Specific Merchant Tests
    # get a specific merchant correctly (status code 200)
    def test_get_200(self):
        response = self.payments_api.merchant.get(os.getenv("MERCHANT_ID"))
        self.test_helper.run_tests(self, response)

    # get a specific merchant with wrong id format (status code 422)
    def test_get_422(self):
        response = self.payments_api.merchant.get(0)
        self.test_helper.run_tests(self, response, 422)
    
    # get a specific merchant with a non-existing id (status code 404)
    def test_get_404(self):
        response = self.payments_api.merchant.get(uuid.uuid4())
        self.test_helper.run_tests(self, response, 404)


if __name__ == '__main__':
    unittest.main()
