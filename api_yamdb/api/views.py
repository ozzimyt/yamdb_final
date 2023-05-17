from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .mixins import ListCreateDestroyGenericViewSet
from .permissions import (IsAdminOrReadOnly, IsAdminUser,
                          IsAuthorOrModeRatOrOrAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenSerializer, UserPermissionsSerializer,
                          UserSerializer, UserSignUpSerializer)


class CategoryViewSet(ListCreateDestroyGenericViewSet):
    """ViewSet класс для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyGenericViewSet):
    """ViewSet класс для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    """ViewSet класс для произведений."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'))
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = TitleFilter
    ordering = ('name',)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet класс для модели Отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrModeRatOrOrAdminOrReadOnly]

    def get_titles(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_titles().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_titles())


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet класс для модели Комментариев."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrModeRatOrOrAdminOrReadOnly]

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet класс для модели Пользователей."""
    http_method_names = ['get', 'post', 'delete', 'patch']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated],
        url_name='me',
        url_path='me'
    )
    def self_me(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        if request.method == 'GET':
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        serializer = UserPermissionsSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSignUpView(APIView):
    """ViewSet класс для пользовательской регистрации."""

    def post(self, request):
        USER_VALIDATE_ERROR = 'Имя пользователя уже занято.'
        EMAIL_VALIDATE_ERROR = 'Электронная почта уже занята.'
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user, _ = User.objects.get_or_create(
                username=username, email=email)
        except IntegrityError:
            sign_up_error = (
                EMAIL_VALIDATE_ERROR
                if User.objects.filter(email=email).exists()
                else USER_VALIDATE_ERROR
            )
            return Response(
                sign_up_error,
                status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            message=(
                f'Здравствуйте, {user.username}! '
                f'Ваш код подтверждения регистрации: {confirmation_code}'
            ),
            subject='Сonfirmation code',
            recipient_list=[user.email],
            from_email=settings.EMAIL_NO_REPLY
        )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserSignInView(APIView):
    """ViewSet класс для пользовательской авторизации."""

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.validated_data.get(
            'confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            return Response(
                {'token': str(AccessToken.for_user(user))},
                status=status.HTTP_201_CREATED
            )
        return Response(
            'Неверный confirmation_code', status=status.HTTP_400_BAD_REQUEST
        )
