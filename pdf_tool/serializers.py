from rest_framework import serializers

from pdf_tool.models import File, Url
from pdf_tool.utils import is_pdf


class UrlSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    url = serializers.CharField(required=True)
    is_alive = serializers.BooleanField(required=True)
    files_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Url
        fields = ["id", "url", "is_alive", "files_count"]


class FileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    urls_count = serializers.IntegerField(read_only=True)
    file = serializers.FileField(write_only=True, required=True, validators=[is_pdf])

    class Meta:
        model = File
        fields = ["id", "name", "urls_count", "file"]
