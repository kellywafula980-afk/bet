from rest_framework import serializers
from apps.sports.models import Match
from apps.odds.models import Odd

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

class OddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Odd
        fields = ['id', 'decimal_odds', 'is_active']
