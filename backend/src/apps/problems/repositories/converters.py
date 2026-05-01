from apps.problems.entities import (
    SectionEntity,
    SubjectEntity,
    TagEntity,
    TopicEntity,
)
from apps.problems.models import Section, Subject, Tag, Topic


class SubjectConverter:
    @staticmethod
    def to_entity(model: Subject) -> SubjectEntity:
        return SubjectEntity(
            id=model.pk,
            name=model.name,
            slug=model.slug,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SectionConverter:
    @staticmethod
    def to_entity(model: Section) -> SectionEntity:
        return SectionEntity(
            id=model.pk,
            name=model.name,
            subject_id=model.subject_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class TopicConverter:
    @staticmethod
    def to_entity(model: Topic) -> TopicEntity:
        return TopicEntity(
            id=model.pk,
            name=model.name,
            section_id=model.section_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class TagConverter:
    @staticmethod
    def to_entity(model: Tag) -> TagEntity:
        return TagEntity(
            id=model.pk,
            name=model.name,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
