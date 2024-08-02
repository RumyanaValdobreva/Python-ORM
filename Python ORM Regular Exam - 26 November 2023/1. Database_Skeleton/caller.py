import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions
from django.db.models import Count, Q, Avg
from main_app.models import Author, Article


def get_authors(search_name=None, search_email=None):
    authors = Author.objects.all()

    if search_name is not None and search_email is not None:
        authors = authors.filter(
            Q(full_name__icontains=search_name) &
            Q(email__icontains=search_email)
        )
    elif search_name is not None:
        authors = authors.filter(full_name__icontains=search_name)
    elif search_email is not None:
        authors = authors.filter(email__icontains=search_email)

    if search_name is None and search_email is None:
        return ""

    authors = authors.order_by('-full_name')

    if not authors:
        return ""

    result = []

    for author in authors:
        status = "Banned" if author.is_banned else "Not Banned"
        result.append(f"Author: {author.full_name}, email: {author.email}, status: {status}")

    return "\n".join(result)


def get_top_publisher():
    top_author = Author.objects.annotate(articles_count=Count('articles')).order_by('-articles_count', 'email').first()

    if not top_author or top_author.articles_count == 0:
        return ""

    return f"Top Author: {top_author.full_name} with {top_author.articles_count} published articles."


def get_top_reviewer():
    top_reviewer = Author.objects.annotate(reviews_count=Count('reviews')).order_by('-reviews_count', 'email').first()

    if not top_reviewer or top_reviewer.reviews_count == 0:
        return ""

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.reviews_count} published reviews."


def get_latest_article():
    latest_article = Article.objects.order_by('-published_on').first()

    if not latest_article:
        return ""

    authors = ', '.join(latest_article.authors.order_by('full_name').values_list('full_name', flat=True))

    num_reviews = latest_article.reviews.count()
    avg_rating = latest_article.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    return f"The latest article is: {latest_article.title}. Authors: {authors}. Reviewed: {num_reviews} times. Average Rating: {avg_rating:.2f}."


def get_top_rated_article():
    top_article = Article.objects.annotate(avg_rating=Avg('reviews__rating'), reviews_count=Count('reviews')).filter(reviews_count__gt=0).order_by('-avg_rating', 'title').first()

    if not top_article:
        return ""

    return f"The top-rated article is: {top_article.title}, with an average rating of {top_article.avg_rating:.2f}, reviewed {top_article.reviews_count} times."


def ban_author(email=None):
    if not email:
        return "No authors banned."

    author = Author.objects.filter(email=email).first()
    if not author:
        return "No authors banned."

    num_reviews = author.reviews.count()
    author.reviews.all().delete()
    author.is_banned = True
    author.save()

    return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."
