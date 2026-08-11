from django.db import models
from apps.sports.models import Match

class Market(models.Model):
    name = models.CharField(max_length=50)  # e.g., "1X2"
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='markets')

    def __str__(self):
        return f"{self.match} - {self.name}"

class Selection(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='selections')
    label = models.CharField(max_length=50)  # Home, Draw, Away
    value = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.market.name} - {self.label}"

class Odd(models.Model):
    selection = models.ForeignKey(Selection, on_delete=models.CASCADE, related_name='odds')
    decimal_odds = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.selection} - {self.decimal_odds}"
