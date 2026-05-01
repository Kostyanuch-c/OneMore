from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from apps.problems.models import Section, Subject, Tag, Topic


admin.site.empty_value_display = '-пусто-'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
        'created_at',
        'updated_at',
    )
    list_display_links = (
        'id',
        'name',
    )
    search_fields = (
        'name',
        'slug',
    )
    prepopulated_fields = {
        'slug': ('name',),
    }
    ordering = ('name',)
    readonly_fields = (
        'created_at',
        'updated_at',
    )


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'subject',
        'created_at',
        'updated_at',
    )
    list_display_links = (
        'id',
        'name',
    )
    list_filter = ('subject',)
    search_fields = (
        'name',
        'subject__name',
    )
    autocomplete_fields = ('subject',)
    ordering = (
        'subject__name',
        'name',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    list_select_related = ('subject',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'section',
        'get_subject',
        'created_at',
        'updated_at',
    )
    list_display_links = (
        'id',
        'name',
    )
    list_filter = (
        'section__subject',
        'section',
    )
    search_fields = (
        'name',
        'section__name',
        'section__subject__name',
    )
    autocomplete_fields = ('section',)
    ordering = (
        'section__subject__name',
        'section__name',
        'name',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Topic]:
        return (
            super()
            .get_queryset(request)
            .select_related(
                'section',
                'section__subject',
            )
        )

    @admin.display(description='Предмет', ordering='section__subject__name')
    def get_subject(self, obj: Topic) -> str:
        return obj.section.subject.name


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'created_at',
        'updated_at',
    )
    list_display_links = (
        'id',
        'name',
    )
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = (
        'created_at',
        'updated_at',
    )
