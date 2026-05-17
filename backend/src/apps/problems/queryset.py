from django.db.models import Prefetch, QuerySet


class ProblemQuerySet(QuerySet):  # type: ignore[type-arg]
    def _with_base_detail(self) -> ProblemQuerySet:
        return self.select_related(
            'author',
            'topic__section',
            'topic__section__subject',
        ).prefetch_related(
            'tags',
        )

    def _with_solutions_detail(self) -> ProblemQuerySet:
        from apps.problems.models import Solution  # noqa PLC0415

        return self.prefetch_related(
            Prefetch(
                'solutions',
                queryset=(
                    Solution.objects.select_related('author').order_by(
                        '-is_main', 'created_at'
                    )
                ),
            )
        )

    def for_detail(
        self,
        *,
        with_solutions: bool = False,
    ) -> ProblemQuerySet:
        queryset = self._with_base_detail()

        if with_solutions:
            queryset = queryset._with_solutions_detail()

        return queryset.order_by('-created_at')

    def for_list(self) -> ProblemQuerySet:
        return self._with_base_detail().order_by('-created_at')
