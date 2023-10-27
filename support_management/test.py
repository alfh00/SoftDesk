class IssueListCreateView(CreateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsContributor]
    pagination_class = PageNumberPagination  # Specify pagination class
    

    
    def get_serializer_class(self):
        # Return the appropriate serializer based on the view's action
        if self.request.method == 'POST':
            return IssueCreateSerializer  # Use IssueCreateSerializer for creating issues
        return IssueSerializer 


    def list(self, request, project_id):
        queryset = Issue.objects.filter(project_id=project_id)
        page = self.paginate_queryset(queryset)  # Perform pagination
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
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



class IssueRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    
    serializer_class = IssueSerializer
    permission_classes = [IsAuthorA]

    def get_queryset(self):
        issue_id = self.kwargs.get('pk')
        return Issue.objects.filter(uuid=issue_id)
    
    def get_serializer_class(self):
        # Return the appropriate serializer based on the view's action
        if self.request.method == 'PUT':
            return IssueCreateSerializer  # Use IssueCreateSerializer for creating issues
        return IssueSerializer 
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "The issue has been successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['POST'], permission_classes=[IsContributor])
    def add_comment(self, request, *args, **kwargs):
        instance = self.get_object()
        text = request.data.get('text')  # Get the comment text from the request data

        if text:
            Comment.objects.create(text=text, author=request.user, issue=instance)
            return Response({"message": "Comment added successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Text field is required for adding a comment."}, status=status.HTTP_400_BAD_REQUEST)

    



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer