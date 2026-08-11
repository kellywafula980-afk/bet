import uuid
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from .paystack import Paystack
from apps.wallet.services import WalletService

MIN_DEPOSIT = 20
MIN_WITHDRAWAL = 50

@login_required
def deposit(request):
    # Ensure user has a phone number
    if not request.user.phone_number:
        messages.warning(request, "Please update your profile with a phone number first.")
        return redirect('accounts:profile')

    if request.method == 'POST':
        amount = request.POST.get('amount')
        if not amount:
            messages.error(request, "Amount is required")
            return redirect('payments:deposit')
        try:
            amount = Decimal(amount)
        except:
            messages.error(request, "Invalid amount format")
            return redirect('payments:deposit')
        if amount <= 0:
            messages.error(request, "Amount must be positive")
            return redirect('payments:deposit')
        if amount < MIN_DEPOSIT:
            messages.error(request, f"Minimum deposit is {MIN_DEPOSIT} KES")
            return redirect('payments:deposit')

        # Convert to cents
        amount_cents = int(amount * 100)
        reference = f"DEP-{request.user.id}-{uuid.uuid4().hex[:8]}"
        email = request.user.email or f"{request.user.phone_number}@user.com"

        # Build metadata with phone number
        metadata = {
            'phone': request.user.phone_number,
            'customer': request.user.phone_number,
            'custom_fields': [
                {'display_name': 'Phone', 'variable_name': 'phone', 'value': request.user.phone_number}
            ]
        }

        response = Paystack.initialize_transaction(
            email=email,
            amount=amount_cents,
            reference=reference,
            callback_url=request.build_absolute_uri(reverse('payments:verify')),
            currency='KES',
            channels=['mobile_money', 'card'],
            metadata=metadata
        )

        if response.get('status'):
            request.session['pending_deposit'] = {
                'reference': reference,
                'amount': str(amount)
            }
            # Redirect to Paystack payment page
            return redirect(response['data']['authorization_url'])
        else:
            messages.error(request, f"Paystack error: {response.get('message')}")
            return redirect('payments:deposit')

    # GET: show deposit form with quick amounts
    return render(request, 'wallet/deposit.html')

@login_required
def verify(request):
    reference = request.GET.get('reference')
    if not reference:
        messages.error(request, "No reference provided")
        return redirect('payments:deposit')

    response = Paystack.verify_transaction(reference)
    if response.get('status') and response['data']['status'] == 'success':
        from apps.wallet.models import WalletTransaction
        if WalletTransaction.objects.filter(reference=reference).exists():
            messages.info(request, "This deposit has already been processed.")
            return redirect('wallet:wallet_dashboard')

        amount = Decimal(response['data']['amount']) / 100
        WalletService.credit(request.user, amount, reference, "Paystack deposit")
        messages.success(request, f"Deposit of {amount} KES successful!")
        return redirect('wallet:wallet_dashboard')
    else:
        messages.error(request, "Payment verification failed.")
        return redirect('payments:deposit')

@login_required
def withdraw(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if not amount:
            messages.error(request, "Amount is required")
            return redirect('payments:withdraw')
        try:
            amount = Decimal(amount)
        except:
            messages.error(request, "Invalid amount format")
            return redirect('payments:withdraw')
        if amount <= 0:
            messages.error(request, "Amount must be positive")
            return redirect('payments:withdraw')
        if amount < MIN_WITHDRAWAL:
            messages.error(request, f"Minimum withdrawal is {MIN_WITHDRAWAL} KES")
            return redirect('payments:withdraw')

        try:
            reference = f"WITHDRAW-{request.user.id}-{uuid.uuid4().hex[:8]}"
            WalletService.withdraw(request.user, amount, reference, "Withdrawal request")
            messages.success(request, f"Withdrawal request of {amount} KES submitted. Awaiting approval.")
            return redirect('wallet:wallet_dashboard')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('payments:withdraw')

    return render(request, 'wallet/withdraw.html')
