from django.db import models


class Url(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.TextField(unique=True)
    is_alive = models.NullBooleanField(null=True, blank=True)

    @property
    def files(self):
        return self.file_set.all()

    @property
    def files_count(self):
        return self.file_set.count()


class File(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    urls = models.ManyToManyField(Url)

    @property
    def urls_count(self):
        return self.urls.count()
