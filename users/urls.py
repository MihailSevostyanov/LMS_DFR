from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentsListAPIView, PaymentsCreateAPIView, PaymentsRetrieveAPIView, PaymentsUpdateAPIView, PaymentsDestroyAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)

urlpatterns = [
    path("payments/", PaymentsListAPIView.as_view(), name="payments_list"),
    path("payments/create/", PaymentsCreateAPIView.as_view(), name="payments_create"),
    path("payments/<int:pk>/", PaymentsRetrieveAPIView.as_view(), name="payments_retrieve"),
    path("payments/<int:pk>/update/", PaymentsUpdateAPIView.as_view(), name="payments_update"),
    path("payments/<int:pk>/delete/", PaymentsDestroyAPIView.as_view(), name="payments_delete"),

]

urlpatterns += router.urls