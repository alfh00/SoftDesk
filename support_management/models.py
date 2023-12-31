from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Project(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    project_type = models.CharField(
        max_length=20,
        choices=[
            ('back-end', 'Back-end'),
            ('front-end', 'Front-end'),
            ('iOS', 'iOS'),
            ('Android', 'Android'),
        ]
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contributors = models.ManyToManyField(User, related_name='contributor_projects')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Issue(models.Model):
    STATUS_CHOICES = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Finished', 'Finished'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    TAG_CHOICES = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task'),
    ]
    
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_to')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='To Do')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, default='BUG')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.issue.name}"
