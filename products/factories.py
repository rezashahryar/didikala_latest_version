class ProductFactory(DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.LazyAttribute(lambda x: ' '.join([x.capitalize() for x in faker.words(3)]))
    slug = factory.LazyAttribute(lambda x: '-'.join(x.name.split(' ')).lower())
    description = factory.Faker('paragraph', nb_sentences=5, variable_nb_sentences=True)
    unit_price = factory.LazyFunction(lambda: random.randint(1, 1000) + random.randint(0, 100)/100)
    inventory = factory.LazyFunction(lambda: random.randint(1, 100))