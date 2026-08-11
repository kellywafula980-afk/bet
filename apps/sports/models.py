from django.db import models

class Sport(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class League(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='leagues')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.sport.name})"

class Team(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('live', 'Live'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    )
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='matches')
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    start_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    home_score = models.PositiveSmallIntegerField(default=0)
    away_score = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
