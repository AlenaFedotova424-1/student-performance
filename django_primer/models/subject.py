from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Subject(name="{self.name}")'
