import factory
from factory.faker import Faker


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'authentication.User'

    username = factory.sequence(lambda i: f'user_{i}')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
