from rest_framework import viewsets, status
from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Project, Issue, Comment
from .serializers import ProjectSerializer, ProjectCreateSerializer, IssueSerializer, IssueCreateSerializer, CommentSerializer
from user_management.models import CustomUser as User
from .permissions import IsContributor, IsAuthor, IsAuthorA
from rest_framework.pagination import PageNumberPagination

# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    # queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Project.objects.filter(contributors=self.request.user)
        return Project.objects.all()

    def get_permissions(self):
         if self.action in ['add_contributor', 'remove_contributor', 'update', 'delete']:
              return [IsAuthorA()]

         if self.action not in ['create', 'list']:
              return [IsContributor()]
         return []

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return ProjectCreateSerializer  # For creation
        return ProjectSerializer  

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.save(author=user)
        project.contributors.add(user)

    @action(detail=True, methods=['POST'])
    def add_contributor(self, request, pk=None):
        project = self.get_object()
        contributor_id = request.data.get('contributor_id')
        
        try:
            contributor = User.objects.get(id=contributor_id)

            if contributor in project.contributors.all():
                        return Response({'message': 'Contributor is already part of the project'}, status=status.HTTP_400_BAD_REQUEST)

            project.contributors.add(contributor)
            return Response({'message': 'Contributor added successfully'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'message': 'Contributor not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['POST'])
    def remove_contributor(self, request, pk=None):
        project = self.get_object()
        contributor_id = request.data.get('contributor_id')

        try:
            contributor = User.objects.get(id=contributor_id)

            if contributor not in project.contributors.all():
                return Response({'message': 'Contributor is not part of the project'}, status=status.HTTP_400_BAD_REQUEST)

            project.contributors.remove(contributor)
            return Response({'message': 'Contributor removed successfully'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'message': 'Contributor not found'}, status=status.HTTP_404_NOT_FOUND)


class IssueViewset(viewsets.ModelViewSet):
    
    queryset = Issue.objects.all()
    permission_classes = [IsContributor]  # Adjust the permission as needed

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ['create', 'update']:
            return IssueCreateSerializer
        return IssueSerializer
        
    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        print(project_id)
        serializer.validated_data['project'] = Project.objects.get(uuid=project_id)
        serializer.validated_data['author'] = self.request.user
        serializer.save()

    @action(detail=True, methods=['POST'], permission_classes=[IsContributor])
    def add_comment(self, request, project_id, pk=None):
        issue = self.get_object()
        text = request.data.get('text')

        if text:
            Comment.objects.create(text=text, author=request.user, issue=issue)
            return Response({'message': 'Comment added successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Text field is required for adding a comment'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'], permission_classes=[IsAuthorA])
    def update_comment(self, request, project_id, issue_id, pk=None):
        comment = self.get_comment(pk)

        if comment:
            if comment.author == request.user:
                text = request.data.get('text')

                if text:
                    comment.text = text
                    comment.save()
                    return Response({'message': 'Comment updated successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Text field is required for updating a comment'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'You do not have permission to update this comment'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['DELETE'], permission_classes=[IsAuthorA])
    def delete_comment(self, request, project_id, issue_id, pk=None):
        comment = self.get_comment(pk)

        if comment:
            if comment.author == request.user:
                comment.delete()
                return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'You do not have permission to delete this comment'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    def get_comment(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return None


