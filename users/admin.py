from django.contrib import admin

from users.models import Payments, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = (
        "id",
        "email",
    )


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_filter = (
        "user",
        "date_of_payment",
        "course",
        "lesson",
    )
