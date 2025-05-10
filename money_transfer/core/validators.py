__all__ = ()

import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_date_future(value):
    if isinstance(value, datetime.date):
        value = datetime.datetime.combine(
            value,
            datetime.time.min,
            timezone.get_current_timezone(),
        )

    if value > timezone.now() + datetime.timedelta(days=1):
        raise ValidationError(_('Time needs to be in past time'))
