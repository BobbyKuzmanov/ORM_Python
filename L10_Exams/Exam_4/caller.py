import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Count
from main_app import models

from main_app.models import TennisPlayer


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ""

    queryset = TennisPlayer.objects.all()

    if search_name:
        queryset = queryset.filter(full_name__icontains=search_name)
    if search_country:
        queryset = queryset.filter(country__icontains=search_country)

    players = queryset.order_by('ranking')

    if not players:
        return ""

    return "\n".join(
        f"Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}"
        for player in players
    )


def get_top_tennis_player():
    top_player = TennisPlayer.objects.annotate(num_wins=models.Count('matches_won')).order_by('-num_wins',
                                                                                              'full_name').first()

    if not top_player:
        return ""

    return f"Top Tennis Player: {top_player.full_name} with {top_player.num_wins} wins."


def get_tennis_player_by_matches_count():
    top_player = TennisPlayer.objects.annotate(
        num_matches=Count('matches')
    ).filter(num_matches__gt=0).order_by('-num_matches', 'ranking').first()

    if not top_player:
        return ""

    return f"Tennis Player: {top_player.full_name} with {top_player.num_matches} matches played."


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ""

    tournaments = models.Tournament.objects.filter(surface_type__icontains=surface).annotate(
        num_matches=Count('matches')
    ).order_by('-start_date')

    if not tournaments:
        return ""

    result = []
    for tournament in tournaments:
        result.append(f"Tournament: {tournament.name},"
                      f" start date: {tournament.start_date}, matches: {tournament.num_matches}")

    return "\n".join(result)


def get_latest_match_info():
    latest_match = models.Match.objects.order_by('-date_played', '-id').first()

    if not latest_match:
        return ""

    players = latest_match.players.order_by('full_name')
    player_names = " vs ".join([player.full_name for player in players])

    winner = "TBA" if latest_match.winner is None else latest_match.winner.full_name

    return (f"Latest match played on: {latest_match.date_played}, "
            f"tournament: {latest_match.tournament.name}, "
            f"score: {latest_match.score}, "
            f"players: {player_names}, "
            f"winner: {winner}, "
            f"summary: {latest_match.summary}")


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return "No matches found."

    matches = models.Match.objects.filter(tournament__name=tournament_name).order_by('-date_played')

    if not matches:
        return "No matches found."

    result = []
    for match in matches:
        winner = "TBA" if match.winner is None else match.winner.full_name
        result.append(f"Match played on: {match.date_played}, score: {match.score}, winner: {winner}")

    return "\n".join(result)