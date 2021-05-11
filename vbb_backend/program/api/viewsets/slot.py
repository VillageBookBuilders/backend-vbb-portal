import datetime, logging
from drf_yasg.utils import swagger_auto_schema
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django_filters import rest_framework as filters

from vbb_backend.program.api.serializers.slot import (
    MinimalSlotSerializer,
    SlotSerializer,
)
from vbb_backend.program.models import Computer, Program, Slot
from vbb_backend.users.models import UserTypeEnum

logger = logging.getLogger('django.db.backends')


class SlotViewSet(ModelViewSet):
    queryset = Slot.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SlotSerializer
    lookup_field = "external_id"

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        computer = Computer.objects.get(
            external_id=self.kwargs.get("computer_external_id")
        )

        queryset = queryset.filter(computer=computer)
        if user.is_superuser:
            pass
        elif user.user_type in [UserTypeEnum.HEADMASTER.value]:
            queryset = queryset.filter(computer__program__program_director=user)
        else:
            raise PermissionDenied()
        return queryset

    def get_computer(self):
        return get_object_or_404(
            Computer, external_id=self.kwargs.get("computer_external_id")
        )

    def perform_create(self, serializer):
        serializer.save(computer=self.get_computer())


class ReadOnlySlotViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Slot.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MinimalSlotSerializer
    lookup_field = "external_id"
    
    # def get_slots(self, for_schedule_start, for_schedule_end):
    #     print(f'\n\n\n\n{for_schedule_start}\n\n\n\n')
    #     return Slot.objects.filter(schedule_start__gte=for_schedule_start)

    def get_queryset(self):
        queryset = self.queryset
        start_day_of_week = self.request.query_params.get("start_day_of_week") or 1
        start_hour = self.request.query_params.get("start_hour") or 0
        start_minute = self.request.query_params.get("start_minute") or 0
        for_schedule_start = Slot.DEAFULT_INIT_DATE + datetime.timedelta(
            days=int(start_day_of_week), hours=int(start_hour), minutes=int(start_minute)
        )
        
        end_day_of_week = self.request.query_params.get("end_day_of_the_week") or 7
        end_hour = self.request.query_params.get("end_hour") or 23
        end_minute = self.request.query_params.get("end_minute") or 59
        for_schedule_end = Slot.DEAFULT_INIT_DATE + datetime.timedelta(days=int(end_day_of_week), hours=int(end_hour), minutes=int(end_minute))
        
        return queryset.filter(schedule_start__gte=for_schedule_start)
        # slot = self.get_slots(for_schedule_start, for_schedule_end)
        # slot_set = slot

        # if slot is None:
        #     return self.queryset.none()

        # return slot


