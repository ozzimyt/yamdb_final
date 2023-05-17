from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitlesViewSet, UserSignInView,
                    UserSignUpView, UserViewSet)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('titles', TitlesViewSet, basename='title')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(
        [
            path('signup/', UserSignUpView.as_view(), name='user_signup'),
            path('token/', UserSignInView.as_view(), name='user_signin')
        ]
    ))
]
