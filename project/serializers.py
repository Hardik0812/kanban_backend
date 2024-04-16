from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "deleted",
        ]
        extra_kwargs = {
            "created_by": {"read_only": True},
            "updated_by": {"read_only":True},
        }
