import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_mobile(value):
    if not value.startswith("+234"):
        message = f"Mobile number is invalid. \
            Be sure to include your country's dialling code."
        raise ValidationError(
            _(re.sub(" +", " ", message)), params={"value": value}
        )
