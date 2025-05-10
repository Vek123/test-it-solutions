__all__ = ()

from django.contrib import admin
from django_admin_filters import DateRangePicker

from catalog import models


@admin.register(models.RecordCategory)
class RecordCategoryAdmin(admin.ModelAdmin):
    fields = (
        models.RecordCategory.name_normalize.field.name,
        models.RecordCategory.name.field.name,
        models.RecordCategory.record_types.field.name,
    )
    readonly_fields = (models.RecordCategory.name_normalize.field.name,)
    list_display = (models.RecordCategory.name.field.name,)
    list_display_links = (models.RecordCategory.name.field.name,)


@admin.register(models.RecordSubCategory)
class RecordSubCategoryAdmin(admin.ModelAdmin):
    fields = (
        models.RecordSubCategory.name_normalize.field.name,
        models.RecordSubCategory.name.field.name,
        models.RecordSubCategory.categories.field.name,
    )
    readonly_fields = (models.RecordSubCategory.name_normalize.field.name,)
    list_display = (models.RecordSubCategory.name.field.name,)
    list_display_links = (models.RecordSubCategory.name.field.name,)


@admin.register(models.RecordStatus)
class RecordStatusAdmin(admin.ModelAdmin):
    fields = (
        models.RecordStatus.name_normalize.field.name,
        models.RecordStatus.name.field.name,
    )
    readonly_fields = (models.RecordStatus.name_normalize.field.name,)
    list_display = (models.RecordStatus.name.field.name,)
    list_display_links = (models.RecordStatus.name.field.name,)


@admin.register(models.RecordType)
class RecordTypeAdmin(admin.ModelAdmin):
    fields = (
        models.RecordType.name_normalize.field.name,
        models.RecordType.name.field.name,
    )
    readonly_fields = (models.RecordType.name_normalize.field.name,)
    list_display = (models.RecordType.name.field.name,)
    list_display_links = (models.RecordType.name.field.name,)


@admin.register(models.Record)
class RecordAdmin(admin.ModelAdmin):
    fields = (
        models.Record.created_at.field.name,
        models.Record.total.field.name,
        models.Record.comment.field.name,
        models.Record.record_type.field.name,
        models.Record.category.field.name,
        models.Record.sub_category.field.name,
        models.Record.status.field.name,
    )
    list_display = (
        models.Record.created_at.field.name,
        models.Record.status.field.name,
        models.Record.record_type.field.name,
        models.Record.category.field.name,
        models.Record.sub_category.field.name,
        models.Record.total.field.name,
        models.Record.short_comment,
    )
    list_display_links = (models.Record.created_at.field.name,)
    list_filter = (
        (models.Record.created_at.field.name, DateRangePicker),
        models.Record.status.field.name,
        models.Record.category.field.name,
        models.Record.sub_category.field.name,
    )

    class Media:
        css = {
            'all': ('css/dtp-custom.css',),
        }

    def get_readonly_fields(self, request, obj):
        if obj:
            return (models.Record.created_at.field.name,)

        return ()
