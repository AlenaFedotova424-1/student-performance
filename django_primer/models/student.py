from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=200, null=False)
    surname = models.CharField(max_length=200, null=False)
    email = models.EmailField(null=False)
    group = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер группы')

    @property
    def fio(self):
        return f'{self.name} {self.surname}'

    def __str__(self):
        return f'{self.fio} ({self.email})'

    def __repr__(self):
        return f'Student(name="{self.name}", name="{self.surname}", name="{self.email}")'
