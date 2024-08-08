from django.contrib.auth.models import AbstractUser
from django.db import models

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
