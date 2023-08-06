import requests


class BootpayBackend:
    BASE_URL = {
        'development': 'https://dev-api.bootpay.co.kr/v2',
        'stage': 'https://stage-api.bootpay.co.kr/v2',
        'production': 'https://api.bootpay.co.kr/v2'
    }

    def __init__(self, application_id, private_key, mode='production'):
        self.application_id = application_id
        self.private_key = private_key
        self.mode = mode
        self.token = None

    # API entrypoints
    # Comment by GOSOMI
    # @param url:string
    # @returns string
    def __entrypoints(self, url):
        return '/'.join([self.BASE_URL[self.mode], url])

    # Request Rest
    # Comment by GOSOMI
    # @param method: string, url: string, data: object, headers: object
    # @returns ResponseForamt
    def __request(self, method='', url='', data=None, headers={}):
        response = getattr(requests, method)(url, json=data, headers=dict(headers, **{
            'Accept': 'application/json',
            'Authorization': (None if self.token is None else f"Bearer {self.token}")
        }))
        return response.json()

    # Get AccessToken
    # Comment by GOSOMI
    def get_access_token(self):
        response = self.__request(method='post', url=self.__entrypoints('request/token'), data={
            'application_id': self.application_id,
            'private_key': self.private_key
        })
        if 'error_code' not in response:
            self.token = response['access_token']
        return response

    # Get Receipt Payment Data
    # Comment by GOSOMI
    # @param receipt_id: string
    def receipt_payment(self, receipt_id=''):
        return self.__request(method='get', url=self.__entrypoints(f'receipt/{receipt_id}'))

    # certificate
    # Comment by GOSOMI
    # @param receipt_id: string
    def certificate(self, receipt_id=''):
        return self.__request(method='get', url=self.__entrypoints(f'certificate/{receipt_id}'))

    # confirm payment
    # Comment by GOSOMI
    # @param receipt_id: string
    def confirm_payment(self, receipt_id=''):
        return self.__request(method='post', url=self.__entrypoints('confirm'), data={"receipt_id": receipt_id})

    # lookup subscribe billing key
    # Comment by GOSOMI
    # @param receipt_id:string
    def lookup_subscribe_billing_key(self, receipt_id=''):
        return self.__request(method='get', url=self.__entrypoints(f'subscribe/billing_key/{receipt_id}'))

    # request subscribe billing key
    # Comment by GOSOMI
    def request_subscribe_billing_key(self, pg='', order_name='', subscription_id='', card_no='', card_pw='',
                                      card_identity_no='', card_expire_year='', card_expire_month='', price=0,
                                      tax_free=0, extra=None, user=None, metadata=None):
        return self.__request(method='post', url=self.__entrypoints('request/subscribe'), data={
            "pg": pg,
            "order_name": order_name,
            "subscription_id": subscription_id,
            "card_no": card_no,
            "card_pw": card_pw,
            "card_identity_no": card_identity_no,
            "card_expire_year": card_expire_year,
            "card_expire_month": card_expire_month,
            "price": price,
            "tax_free": tax_free,
            "extra": extra,
            "user": user,
            "metadata": metadata
        })

    # request subscribe card payment
    # Comment by GOSOMI
    def request_subscribe_card_payment(self, billing_key='', order_name='', price=0, tax_free=0, card_quota='00',
                                       card_interest=None, order_id='', items=None, user=None, extra=None):
        return self.__request(method='post', url=self.__entrypoints('subscribe/payment'), data={
            "billing_key": billing_key,
            "order_name": order_name,
            "price": price,
            "tax_free": tax_free,
            "card_quota": card_quota,
            "card_interest": card_interest,
            "order_id": order_id,
            "items": items,
            "user": user,
            "extra": extra
        })

    # destroy billing key
    # Comment by GOSOMI
    def destroy_billing_key(self, billing_key=''):
        return self.__request(method='delete', url=self.__entrypoints(f'subscribe/billing_key/{billing_key}'))

    # request user token
    # Comment by GOSOMI
    def request_user_token(self, user_id='', email=None, username=None, gender=None, birth=None, phone=None):
        return self.__request(method='post', url=self.__entrypoints('request/user/token'), data={
            "user_id": user_id,
            "email": email,
            "username": username,
            "gender": gender,
            "birth": birth,
            "phone": phone
        })

    # subscribe payment reserve
    # Comment by GOSOMI
    def subscribe_payment_reserve(self, billing_key='', order_name='', price=0, tax_free=0, order_id='', items=None,
                                  user=None, reserve_execute_at='', feedback_url='', content_type=''):
        return self.__request(method='post', url=self.__entrypoints('subscribe/payment/reserve'), data={
            "billing_key": billing_key,
            "order_name": order_name,
            "price": price,
            "tax_free": tax_free,
            "order_id": order_id,
            "items": items,
            "user": user,
            "reserve_execute_at": reserve_execute_at,
            "feedback_url": feedback_url,
            "content_type": content_type
        })

    # cancel subscribe reserve
    # Comment by GOSOMI
    def cancel_subscribe_reserve(self, reserve_id=''):
        return self.__request(method='delete', url=self.__entrypoints(f'subscribe/payment/reserve/{reserve_id}'))

    def shipping_start(self, receipt_id='', tracking_number='', delivery_corp='', shipping_prepayment=None,
                       shipping_day=None, user=None, company=None):
        return self.__request(method='put', url=self.__entrypoints(f'escrow/shipping/start/{receipt_id}'), data={
            "tracking_number": tracking_number,
            "delivery_corp": delivery_corp,
            "shipping_prepayment": shipping_prepayment,
            "shipping_day": shipping_day,
            "user": user,
            "company": company
        })
