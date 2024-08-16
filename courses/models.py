from django.db import models

from config.settings import AUTH_USER_MODEL

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="courses/photo",
        verbose_name="Превью курса",
        help_text="Добавьте превью курса",
        **NULLABLE,
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание курса"
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец курса",
        help_text="Выберите владельца курса", **NULLABLE
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ("title",)


class Lesson(models.Model):
    title = models.CharField(
        max_length=155,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Выберите курс",
        related_name='course',
        **NULLABLE,
    )
    description = models.TextField(
        verbose_name="Описание урока", help_text="Введите описание урока"
    )
    preview = models.ImageField(
        upload_to="lessons/photo",
        verbose_name="Превью урока",
        help_text="Добавьте превью урока",
        **NULLABLE,
    )
    video_url = models.CharField(
        max_length=300,
        verbose_name="Ссылка на видео урока",
        help_text="Укажите ссылку на видео урока",
        **NULLABLE,
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец урока",
        help_text="Выберите владельца урока", **NULLABLE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
