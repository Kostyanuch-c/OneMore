from django.contrib.auth import get_user_model

import factory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@test.local')
    is_active = True

    @factory.post_generation
    def unusable_password(self, create, extracted, **kwargs):  # noqa
        if not create:
            return
        self.set_unusable_password()
        self.save(update_fields=['password'])
