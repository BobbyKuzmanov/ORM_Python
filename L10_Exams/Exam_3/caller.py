import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Article, Review
from django.db.models import Avg, Count


def get_authors(search_name=None, search_email=None):
    authors = Author.objects.all()

    if search_name is not None and search_email is not None:
        authors = authors.filter(full_name__icontains=search_name, email__icontains=search_email)
    elif search_name is not None:
        authors = authors.filter(full_name__icontains=search_name)
    elif search_email is not None:
        authors = authors.filter(email__icontains=search_email)
    else:
        return ""

    if not authors.exists():
        return ""

    authors = authors.order_by('-full_name')

    result = []
    for author in authors:
        status = "Banned" if author.is_banned else "Not Banned"
        result.append(f"Author: {author.full_name}, email: {author.email}, status: {status}")

    return "\n".join(result)


def get_top_publisher():
    top_author = Author.objects.annotate(
        num_articles=models.Count('author_articles')
    ).order_by('-num_articles', 'email').first()

    if not top_author or top_author.num_articles == 0:
        return ""

    return f"Top Author: {top_author.full_name} with {top_author.num_articles} published articles."


def get_top_reviewer():

    top_reviewer = Author.objects.annotate(
            num_reviews=models.Count('author_reviews')
        ).order_by('-num_reviews', 'email').first()

    if not top_reviewer or top_reviewer.num_reviews == 0:
        return ""

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.num_reviews} published reviews."


def get_latest_article():
    latest_article = Article.objects.order_by('-published_on').first()

    if not latest_article:
        return ""

    authors = latest_article.authors.order_by('full_name').values_list('full_name', flat=True)
    authors_str = ", ".join(authors)

    num_reviews = latest_article.article_reviews.count()
    avg_rating = latest_article.article_reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    return (f"The latest article is: {latest_article.title}. Authors: {authors_str}."
            f" Reviewed: {num_reviews} times. Average Rating: {avg_rating:.2f}.")


def get_top_rated_article():
    top_article = Article.objects.annotate(
        avg_rating=Avg('article_reviews__rating'),
        num_reviews=Count('article_reviews')
    ).filter(num_reviews__gt=0).order_by('-avg_rating', 'title').first()

    if not top_article:
        return ""

    return f"The top-rated article is: {top_article.title}, with an average rating of {top_article.avg_rating:.2f}, reviewed {top_article.num_reviews} times."

def ban_author(email=None):
    if email is None:
        return "No authors banned."

    try:
        author = Author.objects.get(email=email)
    except Author.DoesNotExist:
        return "No authors banned."

    num_reviews = author.author_reviews.count()
    author.author_reviews.all().delete()
    author.is_banned = True
    author.save()

    return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."