from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from apps.wallet.services import WalletService
from .models import BetSlip, Bet

class BettingService:
    @staticmethod
    def calculate_potential_win(stake, odds_list):
        total_odds = Decimal(1)
        for odd in odds_list:
            total_odds *= Decimal(odd)
        return stake * total_odds

    @staticmethod
    @transaction.atomic
    def place_bet(user, match_odds_pairs, stake):
        if stake <= 0:
            raise ValidationError("Stake must be positive")

        wallet = user.wallet
        if wallet.balance < stake:
            raise ValidationError("Insufficient balance")

        odds_list = []
        bets_data = []
        for match_id, odd_id in match_odds_pairs:
            from apps.odds.models import Odd
            odd = Odd.objects.select_related('selection__market__match').get(id=odd_id)
            if not odd.is_active:
                raise ValidationError(f"Odd for match {odd.selection.market.match} is not active")
            odds_list.append(odd.decimal_odds)
            bets_data.append({
                'match': odd.selection.market.match,
                'odd': odd,
                'odds_at_time': odd.decimal_odds,
            })

        potential_win = BettingService.calculate_potential_win(Decimal(stake), odds_list)
        WalletService.debit(user, stake, "Bet stake")

        betslip = BetSlip.objects.create(
            user=user,
            stake=stake,
            potential_win=potential_win
        )
        for data in bets_data:
            Bet.objects.create(betslip=betslip, **data)

        return betslip
