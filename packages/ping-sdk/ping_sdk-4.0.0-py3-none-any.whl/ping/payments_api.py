from ping.api_resources.payments_api import merchants
from ping.api_resources.payments_api import paymentOrders
from ping.api_resources.payments_api import payments
from ping.api_resources.payments_api import payouts
from ping.api_resources.payments_api import pings
from ping.helper.apiHelper import get_base_url


class PaymentsApi:
    # A controller to access all endpoints in the API.
    def __init__(self, tenant_id="", environment="sandbox"):
        self.tenant_id = tenant_id
        self.environment = environment
        self.base_url = get_base_url(environment)
        self.headers = {
            "Accept": "application/json",
            "tenant_id": tenant_id
            }

    @property
    def merchant(self):
        return Merchant(self.headers, self.base_url)

    @property
    def paymentOrder(self):
        return PaymentOrder(self.headers, self.base_url)

    @property
    def payment(self):
        return Payment(self.headers, self.base_url)
    
    @property
    def payout(self):
        return Payout(self.headers, self.base_url)

    @property
    def ping(self):
        return Ping(self.headers, self.base_url)



class BaseEndpoints:
    # Endpoint classes inherit from this base class
    def __init__(self, headers, base_url):
        self.headers = headers
        self.base_url = base_url


class Merchant(BaseEndpoints):
    # Endpoint class for merchant endpoints
    def list(self):
        return merchants.list(self.headers, self.base_url)

    def create(self, obj):
        return merchants.create(self.headers, self.base_url, obj)

    def get(self, merchant_id):
        return merchants.get(self.headers, self.base_url, merchant_id)


class PaymentOrder(BaseEndpoints):
    # Endpoint class for payment order endpoints
    def list(self, date_from=None, date_to=None):
        return paymentOrders.list(self.headers, self.base_url, date_from, date_to)

    def create(self, split_tree_id, currency):
        return paymentOrders.create(self.headers, self.base_url, split_tree_id, currency)

    def get(self, payment_order_id):
        return paymentOrders.get(self.headers, self.base_url, payment_order_id)

    def update(self, payment_order_id, split_tree_id):
        return paymentOrders.update(self.headers, self.base_url, payment_order_id, split_tree_id)

    def close(self, payment_order_id):
        return paymentOrders.close(self.headers, self.base_url, payment_order_id)

    def split(self, payment_order_id, fast_forward = False):
        return paymentOrders.split(self.headers, self.base_url, payment_order_id, fast_forward)

    def settle(self, payment_order_id, fast_forward = False):
        return paymentOrders.settle(self.headers, self.base_url, payment_order_id, fast_forward)


class Payment(BaseEndpoints):
    # Endpoint class for payment endpoints
    def initiate(self, obj, payment_order_id):
        return payments.initiate(self.headers, self.base_url, obj, payment_order_id)

    def get(self, payment_order_id, payment_id):
        return payments.get(self.headers, self.base_url, payment_order_id, payment_id)


class Payout(BaseEndpoints):
    # Endpoint class for payout endpoints
    def list(self, date_from=None, date_to=None):
        return payouts.list(self.headers, self.base_url, date_from, date_to)
    
    def get(self, payout_id):
        return payouts.get(self.headers, self.base_url, payout_id)


class Ping(BaseEndpoints):
    # Endpoint class for ping endpoints
    def ping_the_api(self):
        return pings.ping_the_api(self.headers, self.base_url)
