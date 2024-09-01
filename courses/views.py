from datetime import datetime, timedelta

import pytz
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from config import settings
from courses.models import Course, Lesson
from courses.paginators import CustomOffsetPagination, CustomPagination
from courses.serializers import (
    CourseDetailSerializer,
    CourseSerializer,
    LessonSerializer,
)
from courses.tasks import send_information_about_course_update
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        course = serializer.save()
        course.save()

        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime_4_hours_ago = datetime.now(zone) - timedelta(hours=4)

        if course.updated_at < current_datetime_4_hours_ago:
            send_information_about_course_update.delay(course.pk)

    def get_permission(self):
        if self.request.user.groups.filter(name="moders").exists():
            if self.action in ["create", "destroy"]:
                self.permission_classes = (~IsModer,)
            elif self.action in ["update", "retrieve"]:
                self.permission_classes = (IsModer,)
        elif self.action != "create":
            self.permission_classes = (IsOwner,)
        return super().get_permission()


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        new_lesson = serializer.save()

        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime_4_hours_ago = datetime.now(zone) - timedelta(hours=4)

        course = get_object_or_404(Course, pk=new_lesson.course.pk)

        if new_lesson.course.updated_at < current_datetime_4_hours_ago:
            send_information_about_course_update.delay(course.pk)

        course.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomOffsetPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )

    def perform_update(self, serializer):
        new_lesson = serializer.save()

        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime_4_hours_ago = datetime.now(zone) - timedelta(hours=4)

        if new_lesson.course.updated_at < current_datetime_4_hours_ago:
            print(
                f"last_upd {new_lesson.course.updated_at}, -4h {current_datetime_4_hours_ago}"
            )

            send_information_about_course_update.delay(new_lesson.course.pk)

        course = Course.objects.get(course=new_lesson.course.pk)
        course.save()


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )

    def perform_update(self, serializer):
        new_lesson = serializer.save()

        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime_4_hours_ago = datetime.now(zone) - timedelta(hours=4)

        course = get_object_or_404(Course, pk=new_lesson.course.pk)

        if new_lesson.course.updated_at < current_datetime_4_hours_ago:
            send_information_about_course_update.delay(course.pk)

        course.save()


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.groups.filter(name="moders").exists():
            self.permission_classes = (~IsModer, IsAuthenticated)
        else:
            self.permission_classes = (IsOwner, IsAuthenticated)

        return super().get_permissions()
