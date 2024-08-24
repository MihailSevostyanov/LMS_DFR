from rest_framework.serializers import ModelSerializer, SerializerMethodField

from courses.models import Course, Lesson
from courses.validators import VideoUrlValidator


class LessonSerializer(ModelSerializer):
    validators = [VideoUrlValidator(field="video_url")]
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(source="course",
        many=True, read_only=True, help_text="Список уроков курса"
    )

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lesson = SerializerMethodField(
        read_only=True, help_text="Число уроков в курсе"
    )
    all_lessons = LessonSerializer(read_only=True, help_text="Список уроков курса"
                               )

    def get_count_lesson(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = ("title", "preview", "description", "count_lesson", "all_lessons")
