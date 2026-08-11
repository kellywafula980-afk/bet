from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.sports.models import Sport, League, Team, Match
from apps.odds.models import Market, Selection, Odd

class Command(BaseCommand):
    help = 'Loads test sports data with matches and odds'

    def handle(self, *args, **options):
        self.stdout.write('Creating test data...')

        # Create Sport
        sport, _ = Sport.objects.get_or_create(name='Football', slug='football')

        # Create League
        league, _ = League.objects.get_or_create(
            sport=sport,
            name='Premier League',
            slug='premier-league',
            country='England'
        )

        # Create Teams
        teams = [
            {'name': 'Manchester United', 'slug': 'man-utd'},
            {'name': 'Liverpool', 'slug': 'liverpool'},
            {'name': 'Chelsea', 'slug': 'chelsea'},
            {'name': 'Arsenal', 'slug': 'arsenal'},
            {'name': 'Manchester City', 'slug': 'man-city'},
            {'name': 'Tottenham', 'slug': 'tottenham'},
        ]
        team_objs = {}
        for t in teams:
            team, _ = Team.objects.get_or_create(name=t['name'], slug=t['slug'])
            team_objs[t['name']] = team

        # Create Matches (some in the future, some past)
        now = timezone.now()
        match_data = [
            (team_objs['Manchester United'], team_objs['Liverpool'], now + timedelta(days=2, hours=15)),
            (team_objs['Chelsea'], team_objs['Arsenal'], now + timedelta(days=3, hours=16)),
            (team_objs['Manchester City'], team_objs['Tottenham'], now + timedelta(days=4, hours=17)),
            (team_objs['Liverpool'], team_objs['Chelsea'], now + timedelta(days=5, hours=18)),
        ]

        matches = []
        for home, away, start in match_data:
            match, _ = Match.objects.get_or_create(
                league=league,
                home_team=home,
                away_team=away,
                start_time=start,
                defaults={'status': 'pending'}
            )
            matches.append(match)

        # Create Market (1X2) for each match and selections + odds
        for match in matches:
            market, _ = Market.objects.get_or_create(
                match=match,
                name='1X2'
            )
            # Create selections: Home, Draw, Away
            home_selection, _ = Selection.objects.get_or_create(
                market=market,
                label='Home',
                value='1'
            )
            draw_selection, _ = Selection.objects.get_or_create(
                market=market,
                label='Draw',
                value='X'
            )
            away_selection, _ = Selection.objects.get_or_create(
                market=market,
                label='Away',
                value='2'
            )

            # Create odds (random-ish)
            import random
            Odd.objects.get_or_create(
                selection=home_selection,
                defaults={
                    'decimal_odds': round(random.uniform(1.5, 3.0), 2),
                    'is_active': True
                }
            )
            Odd.objects.get_or_create(
                selection=draw_selection,
                defaults={
                    'decimal_odds': round(random.uniform(3.0, 5.0), 2),
                    'is_active': True
                }
            )
            Odd.objects.get_or_create(
                selection=away_selection,
                defaults={
                    'decimal_odds': round(random.uniform(2.0, 4.0), 2),
                    'is_active': True
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Created {len(matches)} matches with odds.'))
