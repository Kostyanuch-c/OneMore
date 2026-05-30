from apps.problems.repositories import SectionRepository


class SectionService:
    repository = SectionRepository()

    def get_all_section_count(self) -> int:
        return self.repository.get_section_count(filters=None)
