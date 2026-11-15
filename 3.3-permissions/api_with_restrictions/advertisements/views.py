from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.viewsets import ModelViewSet

from advertisements.serializers import AdvertisementSerializer
from advertisements.models import Advertisement, AdvertisementStatusChoices
from advertisements.filters import AdvertisementFilter
from advertisements.permissions import IsOwnerOrReadOnly


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        """Черновики видны только автору."""
        user = self.request.user
        queryset = Advertisement.objects.all()

        # Авторизованный пользователь видит все не-черновики + свои черновики.
        if user.is_authenticated:
            return queryset.exclude(status=AdvertisementStatusChoices.DRAFT) | queryset.filter(creator=user)

        # Аноним видит только не-черновики.
        return queryset.exclude(status=AdvertisementStatusChoices.DRAFT)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []
