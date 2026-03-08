from faker import Faker
from factory import fuzzy, LazyAttribute
import factory
from app.models import Client, Parking

fake = Faker('ru_RU')


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = None
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('first_name', locale='ru_RU')
    surname = factory.Faker('last_name', locale='ru_RU')
    credit_card = factory.Faker('credit_card_number')
    car_number = LazyAttribute(
        lambda
            o: f"{fake.random_uppercase_letter()}{fake.random_int(100, 999)}{fake.random_uppercase_letter()}{fake.random_int(10, 99)}{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}"
    )


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = None
        sqlalchemy_session_persistence = 'commit'

    address = factory.Faker('address', locale='ru_RU')
    opened = True
    count_places = fuzzy.FuzzyInteger(10, 50)
    count_available_places = LazyAttribute(lambda o: o.count_places)
