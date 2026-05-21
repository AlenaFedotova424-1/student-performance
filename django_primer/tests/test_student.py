import pytest

from django_primer.models import Student


@pytest.mark.django_db
def test_get_students():
    assert Student.objects.count() == 3

