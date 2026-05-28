from django.db.models import Prefetch, Q, QuerySet


AUTHOR_DEFERRED_FIELDS = (
    'author__password',
    'author__is_superuser',
)


class ProblemQuerySet(QuerySet):  # type: ignore[type-arg]
    def _with_base_detail(
        self,
        *,
        with_subject: bool = False,
    ) -> ProblemQuerySet:
        select_related = [
            'author',
            'topic__section',
        ]

        deferred_fields = [
            *AUTHOR_DEFERRED_FIELDS,
        ]

        if with_subject:
            select_related.append('topic__section__subject')

        return (
            self.select_related(*select_related)
            .defer(*deferred_fields)
            .prefetch_related('tags')
        )

    def _with_solutions_detail(
        self, *, solution_filters: Q | None = None
    ) -> ProblemQuerySet:
        from apps.problems.models import Solution  # noqa PLC0415

        solutions_queryset = Solution.objects.select_related(
            'author',
        ).order_by(
            '-is_main',
            'created_at',
        )

        if solution_filters is not None:
            solutions_queryset = solutions_queryset.filter(solution_filters)

        return self.prefetch_related(
            Prefetch(
                'solutions',
                queryset=solutions_queryset,
            )
        )

    def for_detail(
        self,
        *,
        with_solutions: bool = False,
        with_subject: bool = False,
        solution_filters: Q | None = None,
    ) -> ProblemQuerySet:
        queryset = self._with_base_detail(with_subject=with_subject)

        if with_solutions:
            queryset = queryset._with_solutions_detail(
                solution_filters=solution_filters,
            )

        return queryset.order_by('-created_at')

    def for_list(self, *, with_subject: bool = False) -> ProblemQuerySet:
        return self._with_base_detail(
            with_subject=with_subject,
        ).order_by('-created_at')
