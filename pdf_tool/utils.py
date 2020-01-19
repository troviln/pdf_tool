from urlparse import urlparse

import PyPDF2
import requests
from rest_framework import status
from rest_framework.exceptions import ValidationError


def find_urls_in_pdf(pdf_file):
    urls = set()

    pdf = PyPDF2.PdfFileReader(pdf_file)
    key = "/Annots"
    uri = "/URI"
    ank = "/A"

    for page in range(pdf.getNumPages()):
        page_sliced = pdf.getPage(page)
        page_object = page_sliced.getObject()
        if key in page_object.keys():
            ann = page_object[key]
            for a in ann:
                u = a.getObject()
                if uri in u[ank].keys():
                    url = u[ank][uri]
                    # get url and check if it is valid
                    if is_url(url):
                        # add is_alive attribute
                        urls.add((url, is_alive(url)))

    return urls


def is_pdf(data):
    file_type = data.content_type.split("/")[1]
    if file_type != "pdf":
        raise ValidationError(
            u"Wrong file type .{}. Support only .pdf type.".format(file_type),
            code=status.HTTP_400_BAD_REQUEST
        )


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_alive(url):
    request = requests.get(url)
    if request.status_code == 200:
        return True
    else:
        return False
