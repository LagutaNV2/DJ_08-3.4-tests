from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from students.filters import CourseFilter
from students.models import Course
from students.serializers import CourseSerializer
from django.conf import settings


class CoursesViewSet(ModelViewSet):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = CourseFilter
    
    # def perform_create(self, serializer):
    #     course = serializer.validated_data['course']
    #     if course.students.count() >= settings.MAX_STUDENTS_PER_COURSE:
    #         raise ValidationError('Превышен лимит 20 человек на 1 курс!')
    #     return super().perform_create(serializer)
