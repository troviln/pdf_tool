import os

from rest_framework.test import APITestCase

from pdf_tool.models import Url, File
from pdf_tool.serializers import UrlSerializer, FileSerializer


class RetrieveTestCase(APITestCase):
    def setUp(self):
        self.urls = [
            Url.objects.create(url=u"https://stackoverflow.com/", is_alive=True),
            Url.objects.create(url=u"https://google.com/", is_alive=True),
            Url.objects.create(url=u"https://pikabu1.com/", is_alive=False),  # shared url
            Url.objects.create(url=u"https://test.com/", is_alive=False),
        ]
        self.file_obj_1 = File.objects.create(name=u"name.pdf")
        self.file_obj_2 = File.objects.create(name=u"name_2.pdf")
        self.urls_1 = self.file_obj_1.urls = self.urls[:3]
        self.urls_2 = self.file_obj_2.urls = self.urls[2:]
        self.files = [self.file_obj_1, self.file_obj_2]

    def test_can_get_file_details(self):
        response = self.client.get(u"/api/files/{}/".format(self.file_obj_1.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, FileSerializer(self.file_obj_1).data)

    def test_can_get_files_list(self):
        response = self.client.get(u"/api/files/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, FileSerializer(self.files, many=True).data)

    def test_can_get_file_urls_details(self):
        response = self.client.get(u"/api/files/{}/urls".format(self.file_obj_1.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, UrlSerializer(self.urls_1, many=True).data)

    def test_can_get_urls_list(self):
        response = self.client.get(u"/api/urls/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, UrlSerializer(self.urls, many=True).data)


class CreateTestCase(RetrieveTestCase):
    def setUp(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.test_pdf_file = open(os.path.join(__location__, u"pdf.pdf"))
        response = self.client.post(u"/api/files/", data={"file": self.test_pdf_file})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, FileSerializer(response.data).data)

        self.file_obj_1 = File.objects.get(id=response.data["id"])
        self.files = [self.file_obj_1]
        self.urls_1 = self.urls = [i for i in self.file_obj_1.urls.all()]

    def tearDown(self):
        self.test_pdf_file.close()
