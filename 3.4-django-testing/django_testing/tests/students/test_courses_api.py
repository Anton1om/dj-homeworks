import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course

BASE_URL = '/api/v1/courses/'
TEST_QUANTITY = 10


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_course(client, student_factory, course_factory):
    course = course_factory(_quantity=1, students = student_factory(_quantity=TEST_QUANTITY))

    response = client.get(f'{BASE_URL}{course[0].id}/')

    assert response.status_code == 200
    data = response.json()
    assert data['id']==course[0].id


@pytest.mark.django_db
def test_get_course_list(client, course_factory):
    courses = course_factory(_quantity=TEST_QUANTITY, make_m2m=True)

    response = client.get(BASE_URL)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, course in enumerate(data):
        assert course['id'] == courses[i].id


@pytest.mark.django_db
def test_course_filter_by_id(client, course_factory):
    courses = course_factory(_quantity=TEST_QUANTITY, make_m2m=True)
    course = courses[0]

    response = client.get(f'{BASE_URL}?id={course.id}')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id']==course.id


@pytest.mark.django_db
def test_course_filter_by_name(client, course_factory):
    courses = course_factory(_quantity=TEST_QUANTITY, make_m2m=True)
    course = courses[0]

    response = client.get(f'{BASE_URL}?name={course.name}')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name']==course.name


@pytest.mark.django_db
def test_create_course(client, student_factory):
    students = student_factory(_quantity=TEST_QUANTITY)
    course_data = {'name': 'python', 'students': [s.id for s in students]}

    response = client.post(BASE_URL, data=course_data)

    assert response.status_code == 201
    data = response.json()
    assert data['name']==course_data['name']
    assert set(data['students']) == {s.id for s in students}


@pytest.mark.django_db
def test_update_course(client, student_factory, course_factory):
    course = course_factory(_quantity=1, students = student_factory(_quantity=3))
    patched_data = {'name': 'python'}

    response = client.patch(f'{BASE_URL}{course[0].id}/', data=patched_data)

    assert response.status_code == 200
    data = response.json()
    assert data['id']==course[0].id
    assert data['name']==patched_data['name']


@pytest.mark.django_db
def test_delete_course(client, student_factory, course_factory):
    courses = course_factory(_quantity=TEST_QUANTITY, make_m2m=True)
    course = courses[0]

    response = client.delete(f'{BASE_URL}{course.id}/')
    assert response.status_code == 204

    result = client.get(BASE_URL)
    assert len(result.json()) == TEST_QUANTITY-1
    assert client.get(f'{BASE_URL}{course.id}/').status_code == 404