# -*- coding: utf-8 -*-
from collections import defaultdict
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Student, Subject, Score
from django.shortcuts import redirect, get_object_or_404
from django.views import View


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        scores = Score.objects.all()
        student_scores = defaultdict(dict)

        subjects = [subject.name for subject in Subject.objects.all().order_by('name')]

        for score in scores:
            subject_name = score.subject.name
            student_scores[score.student][subject_name] = score.value

        all_students = Student.objects.all()
        for student in all_students:
            if student not in student_scores:
                student_scores[student] = {}

        student_statistics = []
        for student, scores_dict in student_scores.items():
            scores_list = []
            total_score = 0
            score_count = 0

            for subject in subjects:
                if subject in scores_dict:
                    score_value = scores_dict[subject]
                    scores_list.append(f'{score_value:.1f}')
                    total_score += score_value
                    score_count += 1
                else:
                    scores_list.append('-')

            average_score = round(total_score / score_count, 2) if score_count > 0 else 0

            student_statistics.append({
                'student': student,
                'scores': scores_list,
                'average': average_score
            })
        best_student = None
        worst_student = None
        best_avg = -1
        worst_avg = 6
        for statistic in student_statistics:
            average = statistic['average']
            if average > 0:
                if average > best_avg:
                    best_avg = average
                    best_student = statistic
                if average < worst_avg:
                    worst_avg = average
                    worst_student = statistic

        context.update(
            {
                'subjects': subjects,
                'student_statistics': student_statistics,
                'best_student': best_student,
                'worst_student': worst_student,
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

class SubjectListView(TemplateView):
    template_name = 'subject_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subjects"] = Subject.objects.all().order_by('name')
        return context

class SubjectCreateView(CreateView):
    model = Subject
    fields = ['name']
    template_name = 'subject_form.html'
    success_url = reverse_lazy('subject_list')

class SubjectUpdateView(UpdateView):
    model = Subject
    fields = ['name']
    template_name = 'subject_form.html'
    success_url = reverse_lazy('subject_list')

class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'subject_confirm_delete.html'
    success_url = reverse_lazy('subject_list')


class ScoreListView(TemplateView):
    template_name = 'score_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['scores'] = Score.objects.select_related('student', 'subject').all().order_by('-id')
        context['students'] = Student.objects.all().order_by('surname')
        context['subjects'] = Subject.objects.all().order_by('name')

        return context

class ScoreAddView(CreateView):
    def post(self, request, student_id, subject_id):
        value = request.POST.get('value')
        student = get_object_or_404(Student, id=student_id)
        subject = get_object_or_404(Subject, id=subject_id)

        score, created = Score.objects.get_or_create(
            student=student,
            subject=subject,
            defaults={'value': value}
        )
        if not created:
            score.value = value
            score.save()

        return redirect('score_list')

class ScoreEditView(UpdateView):
    model = Score
    fields = ['value']
    template_name = 'score_form.html'
    def get_success_url(self):
        return reverse_lazy('index')

class ScoreDeleteView(DeleteView):
    model = Score
    template_name = 'score_confirm_delete.html'
    def get_success_url(self):
        return reverse_lazy('index')



