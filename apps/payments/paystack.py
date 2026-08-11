import requests
from django.conf import settings

class Paystack:
    BASE_URL = 'https://api.paystack.co'

    @classmethod
    def initialize_transaction(cls, email, amount, reference, callback_url=None, currency='KES', channels=None, metadata=None):
        """
        amount: in the smallest currency unit (e.g., cents for KES)
        currency: 'KES', 'NGN', etc.
        channels: list of payment channels, e.g., ['mobile_money', 'card']
        metadata: dict with extra info (e.g., phone number)
        """
        url = f"{cls.BASE_URL}/transaction/initialize"
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'email': email,
            'amount': amount,
            'reference': reference,
            'callback_url': callback_url or settings.PAYSTACK_CALLBACK_URL,
            'currency': currency,
        }
        if channels:
            data['channels'] = channels
        if metadata:
            data['metadata'] = metadata

        response = requests.post(url, json=data, headers=headers)
        return response.json()

    @classmethod
    def verify_transaction(cls, reference):
        url = f"{cls.BASE_URL}/transaction/verify/{reference}"
        headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
        response = requests.get(url, headers=headers)
        return response.json()
