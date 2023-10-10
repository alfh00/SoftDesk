from django.contrib import admin

from .models import Project, Issue, Comment  
# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'project_type', 'author')
    list_filter = ('project_type',)
    search_fields = ('name', 'author__username')

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','project', 'status', 'priority', 'tag')
    list_filter = ('priority',)

# admin.site.register(Project, ProjectAdmin)
# admin.site.register(Issue)
admin.site.register(Comment)
