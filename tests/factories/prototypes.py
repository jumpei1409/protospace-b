# tests/factories/prototypes.py
import factory
from prototypes.models import Prototype
from tests.factories.users import UserFactory

class PrototypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Prototype

    title = factory.Faker('sentence', nb_words=4)
    catchphrase = factory.Faker('sentence', nb_words=8)
    concept = factory.Faker('text', max_nb_chars=200)
    image = factory.django.ImageField(color='blue')
    user = factory.SubFactory(UserFactory)