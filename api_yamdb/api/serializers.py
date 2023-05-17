from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .validators import validate_year
from .mixins import UsernameValidatorMixin
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.validators import validate_username


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, value):
        return TitleReadSerializer(value, context=self.context).data


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    category = CategorySerializer(
        read_only=True,
    )
    genre = GenreSerializer(
        many=True,
        read_only=True,
    )
    rating = serializers.IntegerField(read_only=True,)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'genre', 'category', 'description', 'rating',
        )
        read_only_fields = (
            'id', 'name', 'year', 'genre', 'category', 'description', 'rating',
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review(оценивания)."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        if self.context.get('request').method == 'POST':
            author = self.context.get('request').user
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, id=title_id)
            if Review.objects.filter(title_id=title.id,
                                     author=author).exists():
                raise ValidationError(
                    'Может существовать только один отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment(Комментирования)."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class UserSerializer(serializers.ModelSerializer, UsernameValidatorMixin):
    """Сериализатор для модели пользователей."""

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


class UserPermissionsSerializer(UserSerializer):
    """Сериализатор для проверки прав пользователей ."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class UserSignUpSerializer(serializers.Serializer, UsernameValidatorMixin):
    """Сериализатор для пользовательского входа."""

    username = serializers.CharField(
        max_length=settings.FIELD_LIMIT['username'],
        required=True,
        validators=[validate_username]
    )
    email = serializers.EmailField(
        max_length=settings.FIELD_LIMIT['email'],
        required=True,
        allow_blank=False,
        allow_null=False
    )


class TokenSerializer(serializers.Serializer, UsernameValidatorMixin):
    """Сериализатор для выдачи токена пользователям (Регистрации)."""

    username = serializers.CharField(
        max_length=settings.FIELD_LIMIT['username'],
        required=True,
        validators=[validate_username]
    )
    confirmation_code = serializers.CharField(required=True)
