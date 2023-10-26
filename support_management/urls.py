from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, IssueListCreateView, CommentViewSet, IssueRetrieveUpdateDestroyView 


router = DefaultRouter()

# Register the ProjectViewSet with the router
router.register('projects', ProjectViewSet, basename='project')

# Define your URL patterns
urlpatterns = [
    # URL patterns for project-related views
    path('', include(router.urls)),

    # # URL patterns for issue-related views
    path('projects/<uuid:project_id>/issues/', IssueListCreateView.as_view()),
    path('projects/<uuid:project_id>/issues/<uuid:pk>/', IssueRetrieveUpdateDestroyView.as_view()),

    # # URL patterns for comment-related views
    # path('api/projects/<int:project_id>/issues/<int:issue_id>/comments/', CommentListView.as_view(), name='comment-list'),
    # path('api/projects/<int:project_id>/issues/<int:issue_id>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),

    # Other URL patterns for your views
]

