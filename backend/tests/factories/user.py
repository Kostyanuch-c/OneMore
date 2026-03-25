from django.contrib.auth import get_user_model

import factory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        skip_postgeneration_save = True

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    is_active = True

    @factory.post_generation
    def unusable_password(self, create, extracted, **kwargs):  # noqa
        if not create:
            return
        self.set_unusable_password()
        self.save(update_fields=['password'])
