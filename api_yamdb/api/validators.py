import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    if value > dt.date.today().year:
        raise ValidationError(
            'Год выпуска не может быть позже текущего года'
            f'Выбранный год {value}')
    return value
