# setup_test_data.py
import random
from faker import Faker
from datetime import datetime, timedelta

from django.db import transaction
from django.core.management.base import BaseCommand

from blog.models import Category, Blog
from blog.factories import (
    CategoryFactory, BlogFactory
)

faker = Faker()

list_of_models = [Category, Blog]

NUM_CATEGORIES = 100
NUM_BLOGS = 10000


class Command(BaseCommand):
    help = "Generates fake data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = list_of_models
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...\n")

        # Categories data
        print(f"Adding {NUM_CATEGORIES} categories...", end='')
        all_categories = [CategoryFactory()]
        print('DONE')

        # Products data
        print(f"Adding {NUM_BLOGS} product...", end='')
        all_blogs = list()
        for _ in range(NUM_BLOGS):
            new_product = BlogFactory(category_id=random.choice(all_categories).id)
            new_product.datetime_created = faker.date_time_ad(start_datetime=datetime(2022,1,1), end_datetime=datetime(2023,1,1))
            new_product.datetime_modified = new_product.datetime_created + timedelta(hours=random.randint(1, 5000))
            all_blogs.append(new_product)
        print('DONE')




