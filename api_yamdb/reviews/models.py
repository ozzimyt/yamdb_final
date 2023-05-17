from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.validators import validate_year
from .base_models import BaseModelGenreCategory, BaseModelReviewComment


class Category(BaseModelGenreCategory):
    """Модель для категорий."""

    class Meta(BaseModelGenreCategory.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Genre(BaseModelGenreCategory):
    """Модель для жанров."""

    class Meta(BaseModelGenreCategory.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    """Модель для произведений."""
    name = models.TextField(
        'Название произведения',
        max_length=settings.FIELD_LIMIT['name'],
        db_index=True,
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        blank=True,
        validators=[validate_year],
        db_index=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Название категории',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Название жанра',
        blank=True,
        db_index=True,
        related_name='titles',
    )
    description = models.TextField(
        'Описание произведения',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year',)

    def __str__(self):
        return self.name


class Review(BaseModelReviewComment):
    """Модель для представления отзыва."""
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(settings.MIN_SCORE,
                              message='Минимальное значение - 1'),
            MaxValueValidator(settings.MAX_SCORE,
                              message='Максимальное значение - 10')
        ],
        default=settings.MIN_SCORE,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        null=True,
    )

    class Meta(BaseModelReviewComment.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = (
            'author',
            'title',
        )
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(BaseModelReviewComment):
    """Модель комментарий."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Отзыв'
    )

    class Meta(BaseModelReviewComment.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
