from rest_framework.serializers import ModelSerializer

from users.models import Payments, Subscriptions, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class SubscriptionsSerializer(ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = "__all__"
