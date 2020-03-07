import factory
from factory.faker import Faker


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'authentication.User'

    username = factory.sequence(lambda i: f'user_{i}')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')


class TokenFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'authtoken.Token'

    user = factory.SubFactory(UserFactory)
    key = Faker('uuid4')
    created = Faker('date_time')
