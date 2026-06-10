# factories/users.py
import factory
from django.contrib.auth import get_user_model

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    nickname = factory.Faker('first_name')
    email = factory.Faker('email')
    password = factory.Faker('password', length=10)  # 6文字以上を保証
    profile = factory.Faker('text', max_nb_chars=100)
    affiliation = factory.Faker('company')
    position = factory.Faker('job')