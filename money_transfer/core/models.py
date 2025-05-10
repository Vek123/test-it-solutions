__all__ = ()

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

from core.utils import normalize_str


class BaseNameModel(models.Model):
    name = models.CharField(
        _('name'),
        max_length=64,
        help_text=_('Max length is 64'),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return Truncator(self.name).chars(20)


class BaseNameNormalizedModel(BaseNameModel):
    name_normalize = models.CharField(
        _('name (normalized)'),
        max_length=64,
        help_text=_('Generated field based on "name" field'),
        blank=True,
        auto_created=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.name_normalize = normalize_str(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        name_normalize = normalize_str(self.name)
        same_objects = self.__class__.objects.filter(
            name_normalize=name_normalize,
        ).exclude(pk=self.pk)
        if same_objects.exists():
            meta_class = self.__class__._meta
            class_name = meta_class.verbose_name.title()
            field_name = meta_class.get_field(
                'name_normalize',
            ).verbose_name.title()
            raise ValidationError(
                _('%(class_name)s with this %(field_name)s already exists.'),
                params={'class_name': class_name, 'field_name': field_name},
            )

        super().clean()
