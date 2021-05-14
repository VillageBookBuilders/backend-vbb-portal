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
from django.db.models import Q

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

    def get_queryset(self):
        queryset = self.queryset
        start_day_of_week = self.request.query_params.get("start_day_of_week") or 0
        start_hour = self.request.query_params.get("start_hour") or 0
        start_minute = self.request.query_params.get("start_minute") or 0
        schedule_start = Slot.DEAFULT_INIT_DATE + datetime.timedelta(
            days=int(start_day_of_week), hours=int(start_hour), minutes=int(start_minute)
        )
        
        end_day_of_week = self.request.query_params.get("end_day_of_week") or 6
        end_hour = self.request.query_params.get("end_hour") or 23
        end_minute = self.request.query_params.get("end_minute") or 59
        schedule_end = Slot.DEAFULT_INIT_DATE + datetime.timedelta(
            days=int(end_day_of_week), hours=int(end_hour), minutes=int(end_minute)
        )

        computer_id = self.request.query_params.get("computer_id")
        max_students = self.request.query_params.get("max_students")
        language = self.request.query_params.get("language")
        is_mentor_assigned = self.request.query_params.get("is_mentor_assigned")
        is_student_assigned = self.request.query_params.get("is_student_assigned")

        matching_slots = F({
            "schedule_start": schedule_start,
            "schedule_end": schedule_end,
            "computer_id": computer_id,
            "max_students": max_students,
            "is_mentor_assigned": is_mentor_assigned,
            "is_student_assigned": is_student_assigned,
            "language": language,
            }, queryset=queryset)
        return matching_slots.qs

class F(filters.FilterSet):
    language = filters.CharFilter(field_name="language")
    schedule_start = filters.IsoDateTimeFilter(field_name="schedule_start", lookup_expr="gte")
    schedule_end = filters.IsoDateTimeFilter(field_name="schedule_end", lookup_expr="lte")
    computer_id = filters.UUIDFilter(field_name="computer_id__external_id")
    max_students = filters.NumberFilter(field_name="max_students", lookup_expr="lte")
    is_mentor_assigned = filters.BooleanFilter(field_name="is_mentor_assigned")
    is_student_assigned = filters.BooleanFilter(field_name="is_student_assigned")

    class Meta:
        model = Slot
        fields = ("__all__")
