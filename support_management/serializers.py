from rest_framework import serializers
from .models import Project, Issue, Comment
from user_management.models import CustomUser

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username') 

class ProjectSerializer(serializers.ModelSerializer):

    contributors = ContributorSerializer(many=True)
    author = ContributorSerializer()

    class Meta:
        model = Project
        fields = '__all__'

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ['author', 'contributors']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    class Meta:
        model = Issue
        fields = '__all__'

class IssueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        exclude = ['project','author']