__all__ = ()

import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey

from core.models import BaseNameNormalizedModel
from core.validators import validate_date_future


class RecordStatus(BaseNameNormalizedModel):
    class Meta:
        verbose_name = _('record status')
        verbose_name_plural = _('record statuses')


class RecordType(BaseNameNormalizedModel):
    class Meta:
        verbose_name = _('record type')
        verbose_name_plural = _('record types')


class RecordCategory(BaseNameNormalizedModel):
    record_types = models.ManyToManyField(
        RecordType,
        verbose_name=_('type'),
        related_name='categories',
        related_query_name='categories',
    )

    class Meta:
        verbose_name = _('record category')
        verbose_name_plural = _('record categories')


class RecordSubCategory(BaseNameNormalizedModel):
    categories = models.ManyToManyField(
        RecordCategory,
        verbose_name=_('sub category'),
        related_name='sub_categories',
        related_query_name='sub_categories',
    )

    class Meta:
        verbose_name = _('record sub category')
        verbose_name_plural = _('record sub categories')


class Record(models.Model):
    comment = models.TextField(
        _('comment'),
        max_length=65535,
        blank=True,
        null=True,
        help_text=_('Max length is 65535'),
    )
    created_at = models.DateField(
        _('creation date'),
        default=datetime.date.today,
        validators=(validate_date_future,),
    )
    total = models.PositiveIntegerField(
        _('total (rub.)'),
        help_text=_('Enter positive number'),
    )
    category = ChainedForeignKey(
        RecordCategory,
        chained_field='record_type',
        chained_model_field='record_types',
        on_delete=models.RESTRICT,
        verbose_name=_('category'),
        help_text=_('Select "Type" at first'),
    )
    status = models.ForeignKey(
        RecordStatus,
        models.SET_NULL,
        verbose_name=_('status'),
        blank=True,
        null=True,
    )
    sub_category = ChainedForeignKey(
        RecordSubCategory,
        chained_field='category',
        chained_model_field='categories',
        on_delete=models.RESTRICT,
        verbose_name=_('sub category'),
        help_text=_('Select "Category" at first'),
    )
    record_type = models.ForeignKey(
        RecordType,
        on_delete=models.RESTRICT,
        verbose_name=_('type'),
    )

    class Meta:
        default_related_name = 'records'
        verbose_name = _('cash flow record')
        verbose_name_plural = _('cash flow records')

    def __str__(self):
        return f'Record (CF) <{self.record_type} {self.total}>'

    def clean(self):
        super().clean()
        sub_categories = self.category.sub_categories
        categories = self.record_type.categories

        if not sub_categories.filter(id=self.sub_category.id).exists():
            raise ValidationError(
                {
                    Record.sub_category.field.name: _(
                        'Selected sub category'
                        " doesn't belong to the selected category.",
                    ),
                },
            )

        if not categories.filter(id=self.category.id).exists():
            raise ValidationError(
                {
                    Record.category.field.name: _(
                        'Selected category'
                        " doesn't belong to the selected record type.",
                    ),
                },
            )

    def short_comment(self):
        return Truncator(self.comment).chars(40)

    short_comment.short_description = _('short comment')
