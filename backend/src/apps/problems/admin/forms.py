import re

from django import forms
from django.core.exceptions import ValidationError

from apps.problems.models import Section, Subject, Tag, Topic


def normalize_name(value: str) -> str:
    return re.sub(r'\s+', ' ', value.strip())


class NormalizeNameAdminForm(forms.ModelForm):
    def clean_name(self) -> str:
        name = normalize_name(self.cleaned_data['name'])

        if not name:
            raise ValidationError('Название не может быть пустым.')

        return name


class SubjectAdminForm(NormalizeNameAdminForm):
    class Meta:
        model = Subject
        fields = '__all__'  # noqa:DJ007


class SectionAdminForm(NormalizeNameAdminForm):
    class Meta:
        model = Section
        fields = '__all__'  # noqa:DJ007


class TopicAdminForm(NormalizeNameAdminForm):
    class Meta:
        model = Topic
        fields = '__all__'  # noqa:DJ007


class TagAdminForm(NormalizeNameAdminForm):
    class Meta:
        model = Tag
        fields = '__all__'  # noqa:DJ007
