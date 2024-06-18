# def test_example():
#     assert False, "Just test example"

import json
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker

from django.core.exceptions import ValidationError
from django.conf import settings

from students.models import Course, Student


@pytest.fixture()
def client():
    '''
        фикстура для api-client
    '''
    return APIClient()


@pytest.fixture()
def course_factory():
    '''
       фикстура для фабрики курсов
    '''
    
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    
    return factory


@pytest.fixture()
def student_factory():
    '''
        фикстура для фабрики студентов
    '''
    
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    
    return factory


@pytest.mark.django_db
def test_get_one_course(client, course_factory):
    '''
        проверка получения первого курса (retrieve-логика):
        - создаем курс через фабрику;
        - строим урл и делаем запрос через тестовый клиент;
        - проверяем, что вернулся именно тот курс, который запрашивали
    '''
    course = course_factory(_quantity=1)[0]
    
    # url = reverse("courses")
    # response = client.get(f'{url}/{course.id}/')
    
    response = client.get(f'/api/v1/courses/{course.id}/')
    
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course.name

@pytest.mark.django_db
def test_get_courses(client, course_factory):
    '''
        проверка получения списка курсов (list-логика):
        аналогично — сначала вызываем фабрики, затем делаем запрос и проверяем результат
    '''
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name


@pytest.mark.django_db
def test_filter_by_id(client, course_factory):
    '''
        проверка фильтрации списка курсов по id:
           -создаем курсы через фабрику,
           -передать ID одного курса в фильтр,
           -проверить результат запроса с фильтром
    '''

    course_id = course_factory(_quantity=100)[10].id

    response = client.get('/api/v1/courses/', {'id': f'{course_id}'})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == course_id


@pytest.mark.django_db
def test_filter_by_name(client, course_factory):
    ''' проверка фильтрации списка курсов по name'''
    course_name = course_factory(_quantity=100)[10].name

    response = client.get('/api/v1/courses/', {'name': f'{course_name}'})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == course_name


@pytest.mark.django_db
def test_create_course(client):
    ''' тест успешного создания курса '''
    course_data = {'name': 'primer'}

    response = client.post('/api/v1/courses/', data=course_data)

    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'primer'


@pytest.mark.django_db
def test_update_course(client, course_factory):
    '''
        тест успешного обновления курса:
        сначала через фабрику создаём, потом обновляем JSON-данными
    '''
    course = course_factory(_quantity=1)
    course_data = {'name': 'Primer'}

    response = client.patch(f'/api/v1/courses/{course[0].id}/', data=course_data)

    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Primer'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    ''' тест успешного удаления курса'''
    course = course_factory(_quantity=1)[0]

    response = client.delete(f'/api/v1/courses/{course.id}/')

    assert response.status_code == 204
