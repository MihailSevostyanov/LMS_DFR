from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from courses.models import Course, Lesson
from courses.paginators import CustomPagination, CustomOffsetPagination
from courses.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

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


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.groups.filter(name="moders").exists():
            self.permission_classes = (~IsModer, IsAuthenticated)
        else:
            self.permission_classes = (IsOwner, IsAuthenticated)

        return super().get_permissions()
