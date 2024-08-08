from django.urls import path
from rest_framework.routers import SimpleRouter

from courses.views import CourseViewSet, LessonListAPIView, LessonCreateAPIView, LessonUpdateAPIView, LessonDestroyAPIView, LessonRetrieveAPIView
from courses.apps import CoursesConfig

app_name = CoursesConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lessons_list'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lessons_create'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lessons_retrieve'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lessons_update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='Lessons_delete'),
]

urlpatterns += router.urls