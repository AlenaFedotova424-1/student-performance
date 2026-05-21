# -*- coding: utf-8 -*-
from collections import defaultdict
from django.views.generic.base import TemplateView
from .models import Score
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Student


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        scores = Score.objects.all()
        student_scores = defaultdict(dict)

        subjects = set()
        for score in scores:
            subject_name = score.subject.name
            subjects.add(subject_name)
            student_scores[score.student][subject_name] = score.value

        all_students = Student.objects.all()
        for student in all_students:
            if student not in student_scores:
                student_scores[student] = {}

        subjects = sorted(subjects)
        student_statistics = [
            {
                'student': student,
                'scores': [f'{scores.get(subject, "-"):.1f}' if scores.get(subject) else '-' for subject in subjects]
            }
            for student, scores in student_scores.items()
        ]
        context.update(
            {
                'subjects': subjects,
                'student_statistics': student_statistics
            }
        )
        return context

class StudentCreateView(CreateView):
    model = Student
    fields = ['name', 'surname', 'email']
    template_name = 'student_form.html'
    success_url = reverse_lazy('index')

class StudentUpdateView(UpdateView):
    model = Student
    fields = ['name', 'surname', 'email']
    template_name = 'student_form.html'
    success_url = reverse_lazy('index')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_confirm_delete.html'
    success_url = reverse_lazy('index')

