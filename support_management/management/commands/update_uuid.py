# update_uuid.py
from django.core.management.base import BaseCommand
from support_management.models import Project, Issue, Comment
import uuid

class Command(BaseCommand):
    help = 'Update the UUID field with new UUIDs for existing records.'

    def handle(self, *args, **options):
        for record in Project.objects.all():
            record.uuid = uuid.uuid4()
            record.save()
        for record in Issue.objects.all():
            record.uuid = uuid.uuid4()
            record.save()
        for record in Comment.objects.all():
            record.uuid = uuid.uuid4()
            record.save()
