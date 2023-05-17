from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField, TextField

from .validators import validate_username


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICERS = (
        (USER, 'пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'администратор')
    )

    username = CharField(
        'Имя пользователя',
        help_text='Введите имя пользователя',
        max_length=settings.FIELD_LIMIT['username'],
        validators=[validate_username],
        unique=True
    )
    first_name = CharField(
        'Имя',
        help_text='Введите имя',
        max_length=settings.FIELD_LIMIT['first_name'],
        blank=True
    )
    last_name = CharField(
        'Фамилия',
        help_text='Введите фамилию',
        max_length=settings.FIELD_LIMIT['last_name'],
        blank=True
    )
    bio = TextField(
        'Описание пользователя',
        help_text='Введите описание пользователя',
        null=True,
        blank=True
    )
    email = EmailField(
        'Адрес электронной почты',
        help_text='Введите адрес электронной почты',
        unique=True,
        max_length=settings.FIELD_LIMIT['email']
    )
    role = CharField(
        'Права пользователя',
        help_text='Выбирите права пользователя',
        max_length=max(len(role) for _, role in ROLE_CHOICERS),
        choices=ROLE_CHOICERS,
        default=USER
    )
    confirmation_code = CharField(
        'Код подтверждения',
        help_text='Введите код подтверждения',
        max_length=settings.FIELD_LIMIT['confirmation_code'],
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_username_email'
            )
        ]
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return f'{self.username}, {self.email}'
