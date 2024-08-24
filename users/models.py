from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Укажите почту"
    )
    avatar = models.ImageField(upload_to="users/", verbose_name="Аватар", **NULLABLE)
    phone = models.CharField(
        max_length=35,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
        **NULLABLE,
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        help_text="Введите город проживания",
        **NULLABLE,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.email}"


class Payments(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь внесший оплату",
        help_text="Укажите пользователя, внесшего оплату", related_name="payments", **NULLABLE
    )
    date_of_payment = models.DateTimeField(auto_now_add=False, verbose_name="Дата оплаты",
                                           help_text="Введите дату оплаты", **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс",
                               help_text="Укажите оплаченный курс", **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок",
                               help_text="Укажите оплаченный урок", **NULLABLE)
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты", help_text="Введите сумму оплаты")
    payment_method = models.BooleanField(verbose_name="Способ оплаты - наличными", help_text="Укажите способ оплаты")

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f"{self.user} ({self.course if self.course else self.lesson} - {self.payment_amount})"


class Subscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь подписки",
                              help_text="Укажите пользователя подписки", related_name="subscriber")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Подписанный курс",
                               help_text="Укажите подписанный курс", related_name="subscribed_course")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} ({self.course})"