from rest_framework import filters, mixins, viewsets
from users.validators import validate_username

from .permissions import IsAdminOrReadOnly


class ListCreateDestroyGenericViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class UsernameValidatorMixin:

    def username_validation(self, value):
        return validate_username(value)
