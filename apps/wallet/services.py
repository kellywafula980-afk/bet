from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Wallet, WalletTransaction

class WalletService:
    @staticmethod
    def get_or_create_wallet(user):
        wallet, _ = Wallet.objects.get_or_create(user=user)
        return wallet

    @staticmethod
    @transaction.atomic
    def credit(user, amount, reference, description=""):
        if amount <= 0:
            raise ValidationError("Amount must be positive")
        wallet = WalletService.get_or_create_wallet(user)
        wallet.balance += Decimal(amount)
        wallet.save()
        WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type='deposit',
            reference=reference,
            description=description,
            is_successful=True
        )
        return wallet

    @staticmethod
    @transaction.atomic
    def debit(user, amount, description=""):
        if amount <= 0:
            raise ValidationError("Amount must be positive")
        wallet = WalletService.get_or_create_wallet(user)
        if wallet.balance < amount:
            raise ValidationError("Insufficient balance")
        wallet.balance -= Decimal(amount)
        wallet.save()
        WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type='bet_stake',
            reference=f"BET-{user.id}-{hash(description)}",
            description=description,
            is_successful=True
        )
        return wallet

    @staticmethod
    @transaction.atomic
    def withdraw(user, amount, reference, description=""):
        if amount <= 0:
            raise ValidationError("Amount must be positive")
        wallet = WalletService.get_or_create_wallet(user)
        if wallet.balance < amount:
            raise ValidationError("Insufficient balance")
        wallet.balance -= Decimal(amount)
        wallet.save()
        WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type='withdrawal',
            reference=reference,
            description=description,
            is_successful=False  # pending approval
        )
        return wallet
