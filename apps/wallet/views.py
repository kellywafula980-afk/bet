from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def wallet_dashboard(request):
    wallet = request.user.wallet
    transactions = wallet.transactions.all().order_by('-created_at')[:20]
    return render(request, 'wallet/wallet.html', {'wallet': wallet, 'transactions': transactions})
