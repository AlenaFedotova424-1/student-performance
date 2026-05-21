from django.db import models

from .student import Student
from .subject import Subject


class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    value = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f'{self.student.fio}: {self.subject} -> {self.value:.2f}'

    def __repr__(self):
        return f'Student(student="{self.student}", subject="{self.subject}", value="{self.value}")'
