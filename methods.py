import requests
from urls import TestUrls


class ApiMethods:

    @staticmethod
    def user_registration(payload):
        response = requests.post(TestUrls.user_registration, data=payload)
        return response

    @staticmethod
    def user_delete(access_token):
        headers = {'Authorization': f'{access_token}'}
        response = requests.delete(TestUrls.user_delete, headers=headers)
        return response

    @staticmethod
    def user_login(payload):
        response = requests.post(TestUrls.user_authorization, data=payload)
        return response

    @staticmethod
    def user_update(update_payload, access_token):
        headers = {'Authorization': f'{access_token}'}
        response = requests.patch(TestUrls.user_update, data=update_payload, headers=headers)
        return response

    @staticmethod
    def user_update_without_auth(update_payload):
        response = requests.patch(TestUrls.user_update, data=update_payload)
        return response

    @staticmethod
    def create_order(order_payload, access_token=None):
        payload = {'ingredients': [order_payload]}
        headers = {}
        if access_token:
            headers = {'Authorization': f'{access_token}'}
        response = requests.post(TestUrls.order_create, data=payload, headers=headers)
        return response

    @staticmethod
    def get_user_order(access_token=None):
        headers = {}
        if access_token:
            headers = {'Authorization': f'{access_token}'}
        response = requests.get(TestUrls.get_user_orders, headers=headers)
        return response
