import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course


# --------------------------
# Фикстуры
# --------------------------

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make('students.Course', *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make('students.Student', *args, **kwargs)
    return factory


# --------------------------
# Тесты
# --------------------------

@pytest.mark.django_db
def test_get_course_retrieve(api_client, course_factory):
    # Создаем один курс
    course = course_factory()

    # Запрашиваем его по ID
    url = f'/api/courses/{course.id}/'
    response = api_client.get(url)

    # Проверки
    assert response.status_code == 200
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name


@pytest.mark.django_db
def test_get_course_list(api_client, course_factory):

    courses = course_factory(_quantity=5)


    url = '/api/courses/'
    response = api_client.get(url)


    assert response.status_code == 200
    assert len(response.data) == len(courses)


@pytest.mark.django_db
def test_filter_course_by_id(api_client, course_factory):
    courses = course_factory(_quantity=3)

    target_id = courses[0].id

    url = '/api/courses/'
    response = api_client.get(url, data={'id': target_id})

    # Проверки
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == target_id


@pytest.mark.django_db
def test_filter_course_by_name(api_client, course_factory):
    course1 = course_factory(name="Python для начинающих")
    course2 = course_factory(name="Python для продвинутых")

    url = '/api/courses/'
    response = api_client.get(url, data={'name': 'начинающих'})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == course1.name


@pytest.mark.django_db
def test_create_course_success(api_client):
    payload = {
        'name': 'Новый курс',
        'description': 'Описание нового курса'
    }

    url = '/api/courses/'
    response = api_client.post(url, data=payload, format='json')

    assert response.status_code == 201
    assert response.data['name'] == payload['name']
    assert Course.objects.filter(name=payload['name']).exists()


@pytest.mark.django_db
def test_update_course_success(api_client, course_factory):
    course = course_factory()

    payload = {
        'name': 'Обновлённое название',
        'description': 'Новое описание'
    }

    url = f'/api/courses/{course.id}/'
    response = api_client.put(url, data=payload, format='json')

    assert response.status_code == 200
    assert response.data['name'] == payload['name']


@pytest.mark.django_db
def test_delete_course_success(api_client, course_factory):
    course = course_factory()

    url = f'/api/courses/{course.id}/'
    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Course.objects.filter(id=course.id).exists()