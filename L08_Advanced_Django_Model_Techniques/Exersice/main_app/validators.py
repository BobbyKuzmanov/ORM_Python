import re

from django.core.exceptions import ValidationError


def check_name(value):
    if not re.match(r'^[a-zA-Z\s]+$', value):
        raise ValidationError("Name can only contain letters and spaces")