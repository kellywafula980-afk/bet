from django.shortcuts import render, get_object_or_404
from .models import Sport, League, Match

def home(request):
    sports = Sport.objects.all()
    return render(request, 'home.html', {'sports': sports})

def sports_list(request):
    sports = Sport.objects.all()
    return render(request, 'sports/sports.html', {'sports': sports})

def leagues_list(request, sport_slug):
    sport = get_object_or_404(Sport, slug=sport_slug)
    return render(request, 'sports/leagues.html', {'sport': sport})

def matches_list(request, league_slug):
    league = get_object_or_404(League, slug=league_slug)
    matches = league.matches.filter(status='pending')
    return render(request, 'sports/matches.html', {'league': league, 'matches': matches})

def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    return render(request, 'sports/match_detail.html', {'match': match})
