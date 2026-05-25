from django.test import TestCase
from django.test import Client
from django.urls import reverse
from ..models import Student, Subject, Score


class StudentViewsTest(TestCase):

    def setUp(self):
        Student.objects.all().delete()
        Subject.objects.all().delete()
        Score.objects.all().delete()

    def test_index_page_returns_200(self):

        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_student_create_view(self):

        client = Client()
        data = {
            'name': 'Тест',
            'surname': 'Тестовый',
            'email': 'test@test.com',
            'group': 'ИС-21'
        }
        response = client.post(reverse('student_add'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Student.objects.filter(email='test@test.com').exists())

    def test_student_update_view(self):

        student = Student.objects.create(
            name='Иван',
            surname='Иванов',
            email='ivan@test.com'
        )
        client = Client()
        data = {
            'name': 'Петр',
            'surname': 'Петров',
            'email': 'petr@test.com'
        }
        response = client.post(reverse('student_edit', args=[student.id]), data)
        self.assertEqual(response.status_code, 302)
        student.refresh_from_db()
        self.assertEqual(student.name, 'Петр')

    def test_student_delete_view(self):

        student = Student.objects.create(
            name='Иван',
            surname='Иванов',
            email='ivan@test.com'
        )
        client = Client()
        response = client.post(reverse('student_delete', args=[student.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Student.objects.filter(id=student.id).exists())


class SubjectViewsTest(TestCase):


    def setUp(self):
        Student.objects.all().delete()
        Subject.objects.all().delete()
        Score.objects.all().delete()

    def test_subject_list_returns_200(self):
        client = Client()
        response = client.get(reverse('subject_list'))
        self.assertEqual(response.status_code, 200)

    def test_subject_create_view(self):
        client = Client()
        data = {'name': 'Тестовый предмет'}
        response = client.post(reverse('subject_add'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Subject.objects.filter(name='Тестовый предмет').exists())

    def test_subject_update_view(self):
        subject = Subject.objects.create(name='Старый предмет')
        client = Client()
        data = {'name': 'Новый предмет'}
        response = client.post(reverse('subject_edit', args=[subject.id]), data)
        self.assertEqual(response.status_code, 302)
        subject.refresh_from_db()
        self.assertEqual(subject.name, 'Новый предмет')

    def test_subject_delete_view(self):
        subject = Subject.objects.create(name='Предмет для удаления')
        client = Client()
        response = client.post(reverse('subject_delete', args=[subject.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Subject.objects.filter(id=subject.id).exists())


class ScoreViewsTest(TestCase):

    def setUp(self):
        Student.objects.all().delete()
        Subject.objects.all().delete()
        Score.objects.all().delete()

        self.student = Student.objects.create(
            name='Иван',
            surname='Иванов',
            email='ivan@test.com'
        )
        self.subject = Subject.objects.create(name='Математика')

    def test_score_list_returns_200(self):
        client = Client()
        response = client.get(reverse('score_list'))
        self.assertEqual(response.status_code, 200)

    def test_score_add_view(self):
        client = Client()
        response = client.post(
            reverse('score_add', args=[self.student.id, self.subject.id]),
            {'value': 4.5}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Score.objects.filter(student=self.student, subject=self.subject).exists())

    def test_score_update_view(self):
        score = Score.objects.create(
            student=self.student,
            subject=self.subject,
            value=3.0
        )
        client = Client()
        response = client.post(
            reverse('score_edit', args=[score.id]),
            {'value': 5.0}
        )
        self.assertEqual(response.status_code, 302)
        score.refresh_from_db()
        self.assertEqual(score.value, 5.0)

    def test_score_delete_view(self):
        score = Score.objects.create(
            student=self.student,
            subject=self.subject,
            value=4.0
        )
        client = Client()
        response = client.post(reverse('score_delete', args=[score.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Score.objects.filter(id=score.id).exists())


class CalculationsTest(TestCase):

    def setUp(self):
        Student.objects.all().delete()
        Subject.objects.all().delete()
        Score.objects.all().delete()

        self.student1 = Student.objects.create(
            name='Анна',
            surname='Петрова',
            email='anna@test.com'
        )
        self.student2 = Student.objects.create(
            name='Борис',
            surname='Сидоров',
            email='boris@test.com'
        )
        self.subject = Subject.objects.create(name='Математика')

    def test_average_score_calculation(self):

        subject2 = Subject.objects.create(name='Физика')

        Score.objects.create(student=self.student1, subject=self.subject, value=5.0)
        Score.objects.create(student=self.student1, subject=subject2, value=3.0)

        client = Client()
        response = client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        context = response.context
        for stat in context['student_statistics']:
            if stat['student'].id == self.student1.id:
                self.assertEqual(stat['average'], 4.0)

    def test_best_student_detection(self):

        Score.objects.create(student=self.student1, subject=self.subject, value=5.0)
        Score.objects.create(student=self.student2, subject=self.subject, value=3.0)

        client = Client()
        response = client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertEqual(context['best_student']['student'].id, self.student1.id)
        self.assertEqual(context['worst_student']['student'].id, self.student2.id)


class GroupFieldTest(TestCase):

    def setUp(self):
        Student.objects.all().delete()

    def test_student_has_group_field(self):

        student = Student.objects.create(
            name='Иван',
            surname='Иванов',
            email='ivan@test.com',
            group='ИС-21'
        )
        self.assertEqual(student.group, 'ИС-21')

    def test_group_display_in_table(self):

        Student.objects.create(
            name='Иван',
            surname='Иванов',
            email='ivan@test.com',
            group='ИС-21'
        )
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('ИС-21', content)