import random
import factory
from datetime import datetime
from faker import Faker
from factory.django import DjangoModelFactory

from . import models

faker = Faker()


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = models.Category

    name = factory.Faker(
        "sentence",
        nb_words=5,
        variable_nb_words=True
    )


class BlogFactory(DjangoModelFactory):
    class Meta:
        model = models.Blog

    title = factory.Faker(
        "sentence",
        nb_words=5,
        variable_nb_words=True
    )
    slug = factory.Faker(
        "sentence",
        nb_words=3,
        variable_nb_words=False
    )
    description = factory.Faker('paragraph', nb_sentences=1, variable_nb_sentences=False)


    published_date = factory.LazyFunction(
        lambda: faker.date_time_ad(start_datetime=datetime(1990, 1, 1), end_datetime=datetime(2015, 1, 1)))

    status = factory.LazyFunction(
        lambda: random.choice([models.Blog.BLOG_STATUS_PUBLISHED, models.Blog.BLOG_STATUS_DRAFT]))


# class CustomerFactory(DjangoModelFactory):
#     class Meta:
#         model = models.Customer
#
#     first_name = factory.Faker("first_name")
#     last_name = factory.Faker("last_name")
#     email = factory.Faker("email")
#     phone_number = factory.Faker("phone_number")
#     birth_date = factory.LazyFunction(
#         lambda: faker.date_time_ad(start_datetime=datetime(1990, 1, 1), end_datetime=datetime(2015, 1, 1)))





