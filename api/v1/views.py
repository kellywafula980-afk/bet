from rest_framework import viewsets
from apps.sports.models import Match
from .serializers import MatchSerializer

class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.filter(status='pending')
    serializer_class = MatchSerializer
