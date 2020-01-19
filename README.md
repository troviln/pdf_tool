Pdf Tool
======

test application `(python 2.7)`

### Endpoints
 - POST `/api/files/` Uploading a PDF document
 - GET `/api/files/` Returns a set of all the of documents that were uploaded: ids, names and number of URLs that were found for each document
 - GET `/api/files/<file_id>/urls` Returns a set of URLs for a specific document
 - GET `/api/urls/` Returns a set of all URLs found, including the number of documents that contained the URL

#### How to start
1) `pip install -r requirements.txt`
2) `python manage.py migrate`
3) `python manage.py createsuperuser`
4) `python manage.py runserver`
