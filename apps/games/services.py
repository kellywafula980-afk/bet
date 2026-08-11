import random
from decimal import Decimal
from django.core.exceptions import ValidationError
from apps.wallet.services import WalletService
from .models import WheelSpin

class WheelService:
    # Demo mode: very player-friendly, high chance of big wins
    DEMO_MULTIPLIERS = [
        (0.0, 10),
        (0.5, 10),
        (1.0, 15),
        (1.5, 15),
        (2.0, 15),
        (3.0, 12),
        (5.0, 10),
        (10.0, 7),
        (50.0, 6),
    ]

    # Live mode: house edge ~4.1%
    LIVE_MULTIPLIERS = [
        (0.0, 55),
        (0.5, 10),
        (1.0, 15),
        (1.5, 7),
        (2.0, 5),
        (3.0, 3),
        (5.0, 2),
        (10.0, 1),
        (50.0, 0.5),
    ]

    @classmethod
    def spin(cls, user, bet_amount, demo_mode=False, request=None):
        if bet_amount <= 0:
            raise ValidationError("Bet must be positive")

        if demo_mode:
            # Use demo multipliers
            multipliers, weights = zip(*cls.DEMO_MULTIPLIERS)
            # Get demo balance from session (convert to Decimal for safe arithmetic)
            demo_balance = Decimal(str(request.session.get('demo_balance', 1000)))
            if demo_balance < bet_amount:
                raise ValidationError("Insufficient demo balance")
            # Deduct bet
            demo_balance -= bet_amount
            # Choose multiplier
            multiplier = random.choices(multipliers, weights=weights, k=1)[0]
            multiplier = Decimal(str(multiplier))
            win_amount = bet_amount * multiplier
            if win_amount > 0:
                demo_balance += win_amount
            # Save back to session as float (or string)
            request.session['demo_balance'] = float(demo_balance)
            return {
                'multiplier': float(multiplier),
                'win_amount': float(win_amount),
                'new_balance': float(demo_balance),
                'is_demo': True,
            }
        else:
            # Live mode: use real wallet
            wallet = user.wallet
            if wallet.balance < bet_amount:
                raise ValidationError("Insufficient balance")
            multipliers, weights = zip(*cls.LIVE_MULTIPLIERS)
            multiplier = random.choices(multipliers, weights=weights, k=1)[0]
            multiplier = Decimal(str(multiplier))
            win_amount = bet_amount * multiplier

            WalletService.debit(user, bet_amount, "Wheel spin (live)")
            if win_amount > 0:
                WalletService.credit(
                    user,
                    win_amount,
                    f"WHEEL-{user.id}-{random.randint(1000,9999)}",
                    f"Wheel win {multiplier}x"
                )

            spin = WheelSpin.objects.create(
                user=user,
                bet_amount=bet_amount,
                multiplier=multiplier,
                win_amount=win_amount
            )
            return {
                'multiplier': float(multiplier),
                'win_amount': float(win_amount),
                'new_balance': float(user.wallet.balance),
                'is_demo': False,
            }
