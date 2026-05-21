# -*- coding: utf-8 -*-
from collections import defaultdict

from django.views.generic.base import TemplateView

from .models import Score


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

        subjects = sorted(subjects)
        student_statistics = [
            {
                'student': student,
                'scores': [f'{scores[subject]:.1f}' for subject in subjects]
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
