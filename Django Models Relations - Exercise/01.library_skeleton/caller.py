import os
from datetime import date, timedelta

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions

from main_app.models import Author, Book, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Car, Registration


def show_all_authors_with_their_books():
    result = []
    authors = Author.objects.all().order_by('id')

    for author in authors:
        books = Book.objects.filter(author=author)

        if not books:
            continue

        author_books = [book.title for book in books]
        result.append(f"{author.name} has written - {', '.join(author_books)}!")

    return '\n'.join(result)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    return Artist.objects.get(name=artist_name).songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    reviews = product.reviews.all()

    average_rating = sum(rt.rating for rt in reviews) / len(reviews)

    return average_rating


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()


def calculate_licenses_expiration_dates():
    # issue_date + timedelta(days=365)
    licenses = DrivingLicense.objects.order_by('-license_number')
    result = []

    for license in licenses:
        expiration_date = license.issue_date + timedelta(days=365)
        result.append(f"License with number: {license.license_number} expires on {expiration_date}!")

    return '\n'.join(result)


def get_drivers_with_expired_licenses(due_date: date):
    expiration_date = due_date - timedelta(days=365)
    drivers_with_expired_licenses = Driver.objects.filter(license__issue_date__gt=expiration_date)

    return drivers_with_expired_licenses


def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    car.owner = owner
    car.save()

    registration.registration_date = date.today()
    registration.car = car
    registration.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."
