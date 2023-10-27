from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, IssueViewset


router = DefaultRouter()

# Register the ProjectViewSet with the router
router.register('projects', ProjectViewSet, basename='project')
router.register(r'projects/(?P<project_id>[^/.]+)/issues', IssueViewset)

# Define your URL patterns
urlpatterns = [
    # URL patterns for project-related views
    path('', include(router.urls)),
    path('projects/<uuid:project_id>/issues/<uuid:issue_id>/comments/<uuid:pk>/update/', IssueViewset.as_view({'put': 'update_comment'}), name='update-comment'),
    path('projects/<uuid:project_id>/issues/<uuid:issue_id>/comments/<uuid:pk>/delete/', IssueViewset.as_view({'delete':'delete_comment'}), name='delete-comment'),

    # # URL patterns for issue-related views
    # path('projects/<uuid:project_id>/issues/', IssueViewset.as_view)

    # Other URL patterns for your views
]

