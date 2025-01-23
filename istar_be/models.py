from django.db import models


class Animal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "animals"


class PageFormat(models.Model):
    id = models.AutoField(primary_key=True)
    page_number = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.page_number

    class Meta:
        db_table = "pages_format"
