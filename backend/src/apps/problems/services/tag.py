from apps.problems.exceptions import TagNotFoundError
from apps.problems.repositories import TagRepository


class TagService:
    repository = TagRepository()

    def ensure_tags_exist(self, tag_ids: list[int]) -> None:
        if not tag_ids:
            return

        requested_tag_ids = set(tag_ids)
        existing_tag_ids = self.repository.get_existing_tag_ids(
            tag_ids=list(requested_tag_ids),
        )

        missing_tag_ids = requested_tag_ids - existing_tag_ids

        if missing_tag_ids:
            raise TagNotFoundError(
                message='Some tags were not found',
                extra={
                    'field': ['tag_ids'],
                    'missing_tag_ids': sorted(missing_tag_ids),
                },
            )
