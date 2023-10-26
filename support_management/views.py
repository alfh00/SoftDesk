from rest_framework import viewsets, status
from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Project, Issue, Comment
from .serializers import ProjectSerializer, ProjectCreateSerializer, IssueSerializer, IssueCreateSerializer, CommentSerializer
from user_management.models import CustomUser as User
from .permissions import IsContributor, IsAuthor, IsAuthorA

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



class IssueListCreateView(ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsContributor]

    
    def get_serializer_class(self):
        # Return the appropriate serializer based on the view's action
        if self.request.method == 'POST':
            return IssueCreateSerializer  # Use IssueCreateSerializer for creating issues
        return IssueSerializer 


    def list(self, request, project_id):
        # Custom logic to filter and return issues associated with the project
        queryset = Issue.objects.filter(project_id=project_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_id):
        # Change the serializer class for creation
        serializer = IssueCreateSerializer(data=request.data)

        if serializer.is_valid():
            # Get the project_id from the URL (you might need to adjust this depending on your URL structure)
            project_id = self.kwargs.get('project_id')
            author = self.request.user

            # Get the project instance based on project_id
            try:
                project = Project.objects.get(pk=project_id)
            except Project.DoesNotExist:
                return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

            # Assign the project to the issue and save it
            serializer.save(project=project, author=author)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import action

class IssueRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    
    serializer_class = IssueSerializer
    permission_classes = [IsContributor]

    def get_queryset(self):
        issue_id = self.kwargs.get('pk')
        return Issue.objects.filter(uuid=issue_id)
    

    



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer