from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience


class ExperienceSerializer(serializers.ModelSerializer):
    thumbnail_direct_url = serializers.ReadOnlyField()
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "description",
            "category",
            "thumbnail",
            "thumbnail_direct_url",
            "started_at",
            "ended_at",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = [
            "id",
            "thumbnail_direct_url",
            "started_at",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Judul tidak boleh hanya berisi tag HTML."
            )
        return value

    def validate_description(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Deskripsi tidak boleh hanya berisi tag HTML."
            )
        return value

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())
