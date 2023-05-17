from django.conf import settings
from django.db import models

from users.models import User


class BaseModelGenreCategory(models.Model):
    """Абстрактная модель для жанров и категорий."""

    name = models.CharField(
        'Название', max_length=settings.FIELD_LIMIT['name'])
    slug = models.SlugField(
        'Ссылка', max_length=settings.FIELD_LIMIT['slug'], unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class BaseModelReviewComment(models.Model):
    """Абстрактная модель для review и comment"""
    text = models.TextField('Текст отзыва')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text
