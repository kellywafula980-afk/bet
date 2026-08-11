from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .services import BettingService
from apps.sports.models import Match
from apps.odds.models import Odd

@login_required
def place_bet(request):
    if request.method == 'POST':
        odd_ids = request.POST.getlist('odd_ids')
        stake = request.POST.get('stake')
        if not odd_ids or not stake:
            messages.error(request, "Invalid bet data")
            return redirect('betting:place_bet')

        match_odds_pairs = []
        for odd_id in odd_ids:
            odd = get_object_or_404(Odd, id=odd_id)
            match_odds_pairs.append((odd.selection.market.match.id, odd.id))

        try:
            betslip = BettingService.place_bet(request.user, match_odds_pairs, Decimal(stake))
            messages.success(request, f"Bet placed! Potential win: {betslip.potential_win}")
            return redirect('betting:my_bets')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('betting:place_bet')

    matches = Match.objects.filter(status='pending')
    return render(request, 'betting/place_bet.html', {'matches': matches})

@login_required
def my_bets(request):
    betslips = request.user.betslips.all().order_by('-placed_at')
    return render(request, 'betting/my_bets.html', {'betslips': betslips})
