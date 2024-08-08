from rest_framework.serializers import ModelSerializer, SerializerMethodField

from courses.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lesson = SerializerMethodField(
        read_only=True, help_text="Число уроков в курсе"
    )

    def get_count_lesson(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = ("title", "preview", "description", "count_lesson")


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
