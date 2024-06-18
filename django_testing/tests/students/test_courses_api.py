# def test_example():
#     assert False, "Just test example"

import json
import pytest
from django.urls import reverse
from override_settings import override_settings
from rest_framework.test import APIClient
from model_bakery import baker

from django.core.exceptions import ValidationError
from django.conf import settings

from django_testing.settings import MAX_STUDENTS_PER_COURSE
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
def test_get_retrieve_course(client, course_factory):
    '''
        проверка получения первого курса (retrieve-логика):
        - создаем курс через фабрику;
        - строим урл и делаем запрос через тестовый клиент;
        - проверяем, что вернулся именно тот курс, который запрашивали
    '''
    course = course_factory(_quantity=1)[0]
    
    # url = reverse("courses")
    # print(f'{url=}, / {course.id=}')
    # response = client.get(f'{url}/{course.id}/')
   
    response = client.get(f'/api/v1/courses/{course.id}/')
    # print(f'  test1: {response.json()=}')
    
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course.name

@pytest.mark.django_db
def test_get_list_courses(client, course_factory):
    '''
        проверка получения списка курсов (list-логика):
        аналогично — сначала вызываем фабрики, затем делаем запрос и проверяем результат
    '''
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/')
    print(f'  test2: {response.json()=}')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, j in enumerate(data):
        print(f'тест-2 enumerate of data: {i=}, {j=}')
        assert courses[i].name == j['name']


@pytest.mark.django_db
def test_filter_id(client, course_factory):
    '''
        проверка фильтрации списка курсов по id:
           -создаем курсы через фабрику,
           -передать ID одного курса в фильтр,
           -проверить результат запроса с фильтром
    '''
    
    courses = course_factory(_quantity=10)
    course_id = courses[5].id

    response = client.get('/api/v1/courses/', {'id': course_id})
    print(f'  test3: {response.json()=}')
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == course_id


@pytest.mark.django_db
def test_filter_name(client, course_factory):
    ''' проверка фильтрации списка курсов по name'''
    courses = course_factory(_quantity=100)
    course_name = courses[10].name
    
    response = client.get('/api/v1/courses/', {'name': course_name})
    # print(f'  test4: {response.json()=}')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == course_name


@pytest.mark.django_db
def test_create_course(client):
    ''' тест успешного создания курса '''
    course_data = {'name': 'primer'}

    response = client.post('/api/v1/courses/', data=course_data)
    # print(f'  test5: {response.json()=}')

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
    course_id = course[0].id
    new_data = {'name': 'Primer'}

    response = client.patch(f'/api/v1/courses/{course_id}/', data=new_data)
    # print(f'  test6: {response.json()=}')
    
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Primer'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    ''' тест успешного удаления курса'''
    course = course_factory(_quantity=1)
    course_id = course[0].id

    response = client.delete(f'/api/v1/courses/{course_id}/')
    print(f'  test7: {response=}')

    assert response.status_code == 204


# дополнительное задание: ограничить число студентов на курсе
# @pytest.mark.django_db
# # @override_settings(MAX_STUDENTS_PER_COURSE, 2)
# # @pytest.mark.parametrize("count, is_error", [
# #     (settings.MAX_STUDENTS_PER_COURSE - 1, False),
# #     (settings.MAX_STUDENTS_PER_COURSE + 1, True),
# # ])
# def test_max_student(client, course_factory, student_factory):
#     course = course_factory(_quantity=1)[0]
#     students = student_factory(_quantity=20)
#     course.students.extend(*students)
#
#     # if is_error:
#     #     with pytest.raises(ValidationError,
#     #                        match=f"Максимальное число студентов на курсе: {settings.MAX_STUDENTS_PER_COURSE}"):
#     #         course.clean()
#     # else:
#     #     course.clean()
