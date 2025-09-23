import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from django.db.models import Q, Count, Avg, F, Max
from main_app.models import Director, Actor, Movie
from django.db import transaction


def get_top_directors(search_name=None, search_nationality=None):
    # Start with all directors
    directors = Director.objects.all()

    if search_name is not None and search_nationality is not None:
        directors = directors.filter(
            Q(full_name__icontains=search_name) &
            Q(nationality__icontains=search_nationality)
        )
    elif search_name is not None:
        directors = directors.filter(full_name__icontains=search_name)
    elif search_nationality is not None:
        directors = directors.filter(nationality__icontains=search_nationality)
    else:
        return ""

    directors = directors.order_by('full_name')

    if not directors:
        return ""

    result = []
    for director in directors:
        result.append(
            f"Director: {director.full_name}, nationality: {director.nationality},"
            f" experience: {director.years_of_experience}")

    return "\n".join(result)


def get_top_director():
    top_director = Director.objects.annotate(
        num_movies=Count('director_movies')
    ).order_by('-num_movies', 'full_name').first()

    if not top_director:
        return ""

    return f"Top Director: {top_director.full_name}, movies: {top_director.num_movies}."


def get_top_actor():
    top_actor = Actor.objects.annotate(
        num_starring_movies=Count('actor_starring_movies'),
        avg_rating=Avg('actor_starring_movies__rating')
    ).filter(num_starring_movies__gt=0).order_by('-num_starring_movies', 'full_name').first()

    if not top_actor:
        return ""

    starring_movies = top_actor.actor_starring_movies.order_by('title')
    movie_titles = ", ".join([movie.title for movie in starring_movies])

    return (f"Top Actor: {top_actor.full_name}, "
            f"starring in movies: {movie_titles}, "
            f"movies average rating: {top_actor.avg_rating:.1f}")


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(
        num_movies=Count('actor_all_movies')
    ).order_by('-num_movies', 'full_name')[:3]

    result = []
    for actor in actors:
        result.append(f"{actor.full_name}, participated in {actor.num_movies} movies")

    return "\n".join(result)


def get_top_rated_awarded_movie():
    highest_rating = Movie.objects.filter(is_awarded=True).aggregate(Max('rating'))['rating__max']

    if highest_rating is None:
        return ""

    top_movie = Movie.objects.filter(
        is_awarded=True,
        rating=highest_rating
    ).order_by('title').first()

    if top_movie is None:
        return ""

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'

    cast = top_movie.actors.order_by('full_name').values_list('full_name', flat=True)
    cast_string = ", ".join(cast)

    return (
        f"Top rated awarded movie: {top_movie.title}, "
        f"rating: {top_movie.rating:.1f}. "
        f"Starring actor: {starring_actor}. "
        f"Cast: {cast_string}."
    )


def increase_ratings():
    updated_movies = Movie.objects.filter(
        is_classic=True,
        rating__lt=10.0
    ).update(rating=F('rating') + 0.1)

    if updated_movies > 0:
        return f"Rating increased for {updated_movies} movies."
    else:
        return "No ratings increased."


def increase_rating():
    with transaction.atomic():
        classic_movies = Movie.objects.filter(is_classic=True, rating__lt=10.0)

        updated_count = classic_movies.update(
            rating=F('rating') + 0.1
        )

        Movie.objects.filter(rating__gt=10.0).update(rating=10.0)

    if updated_count > 0:
        return f"Rating increased for {updated_count} movies."
    else:
        return "No ratings increased."
