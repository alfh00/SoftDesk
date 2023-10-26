from django.urls import path, include
from .views import RegisterUserView, UsersViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UsersViewSet)

urlpatterns = [
    # Allow any for signing up
    path('register/', RegisterUserView.as_view(), name='register_user'),
    # 'only for staff'
    path('', include(router.urls)),
]
