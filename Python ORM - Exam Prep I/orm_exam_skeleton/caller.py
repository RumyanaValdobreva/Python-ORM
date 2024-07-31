import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Actor, Director, Movie
from django.db.models import Q, Count, Avg, F


# Create queries within functions

def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    query_full_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = Q(query_full_name & query_nationality)
    elif search_name is not None:
        query = query_full_name
    else:
        query = query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ""

    result = []

    for director in directors:
        result.append(f"Director: {director.full_name}, nationality: {director.nationality}, experience: {director.years_of_experience}")

    return "\n".join(result)


def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()

    if not director:
        return ""
    else:
        return f"Top Director: {director.full_name}, movies: {director.num_movies}."


def get_top_actor():
    actor = Actor.objects.prefetch_related('starring_actors_movie').annotate(
        num_movies=Count('starring_actors_movie'),
        avg_rating=Avg('starring_actors_movie__rating')
    ).order_by('-num_movies', 'full_name').first()

    if not actor or not actor.num_movies:
        return ""

    movies = ', '.join(x.title for x in actor.starring_actors_movie.all() if x)

    return f"Top Actor: {actor.full_name}, starring in movies: {movies}, movies average rating: {actor.avg_rating:.1f}"


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(num_movies=Count('actors')).order_by('-num_movies', 'full_name')[:3]

    if not actors or not actors[0].num_movies:
        return ""

    result = []

    for actor in actors:
        result.append(f"{actor.full_name}, participated in {actor.num_movies} movies")

    return "\n".join(result)


def get_top_rated_awarded_movie():
    top_awarded_movie = Movie.objects.select_related('starring_actor').prefetch_related('actors').filter(is_awarded=True)\
        .order_by('-rating', 'title').first()

    if top_awarded_movie is None:
        return ""

    starring_actor = top_awarded_movie.starring_actor.full_name if top_awarded_movie.starring_actor else 'N/A'

    actors_cast = top_awarded_movie.actors.order_by('full_name').values_list('full_name', flat=True)

    cast = ", ".join(actors_cast)

    return f"Top rated awarded movie: {top_awarded_movie.title}, rating: {top_awarded_movie.rating:.1f}. Starring actor: {starring_actor}. Cast: {cast}."


def increase_rating():
    movies_to_update = Movie.objects.filter(is_classic=True, rating__lt=10.0)

    if not movies_to_update:
        return "No ratings increased."

    updated_movies = movies_to_update.count()

    movies_to_update.update(rating=F('rating') + 0.1)

    return f"Rating increased for {updated_movies} movies."