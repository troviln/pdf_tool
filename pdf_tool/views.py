from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from pdf_tool.models import File, Url
from pdf_tool.serializers import FileSerializer, UrlSerializer
from pdf_tool.utils import find_urls_in_pdf


class FileListCreateView(generics.ListCreateAPIView):
    queryset = File.objects
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get file from the request
        file_obj = serializer.initial_data["file"]

        # retrieve file name and urls from it
        found_urls = find_urls_in_pdf(file_obj)
        file_name = file_obj.name
        # get or create url objects from db
        urls_set = set()
        for url in found_urls:
            url_db, _ = Url.objects.get_or_create(url=url[0])
            # set or update is_alive
            url_db.is_alive = url[1]
            url_db.save()
            # bind url with a file
            urls_set.add(url_db)

        # create a new file object into db with passed name and parsed urls
        file_db = File(name=file_name)
        file_db.save()
        file_db.urls = urls_set

        # return a response
        serializer = self.get_serializer(file_db)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FileRetrieveView(generics.RetrieveAPIView):
    queryset = File.objects
    serializer_class = FileSerializer
    lookup_field = "id"


class UrlListView(generics.ListAPIView):
    queryset = Url.objects
    serializer_class = UrlSerializer

    def get_queryset(self):
        # filter by file id if it is passed
        file_id = self.kwargs.get("file_id")
        if file_id:
            return get_object_or_404(File, id=file_id).urls
        return self.queryset.all()
