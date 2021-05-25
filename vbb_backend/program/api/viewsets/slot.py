import datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
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


class SlotFilterSet(filters.FilterSet):
    computer = filters.UUIDFilter(field_name="computer__external_id")
    program = filters.UUIDFilter(field_name="computer__program__external_id")
    max_students = filters.NumberFilter(field_name="max_students", lookup_expr="lte")
    language = filters.CharFilter(field_name="language")
    is_mentor_assigned = filters.BooleanFilter(field_name="is_mentor_assigned")
    is_student_assigned = filters.BooleanFilter(field_name="is_student_assigned")
    

class ReadOnlySlotViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Slot.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MinimalSlotSerializer
    lookup_field = "external_id"
    filterset_class = SlotFilterSet

    def get_queryset(self):
        queryset = self.queryset
        try:
            start_day_of_week = int(self.request.GET.get("start_day_of_week", 0))
        except:
            raise ValidationError({'schedule': 'start_day_of_week must be a integer'})
        try:
            start_hour = int(self.request.GET.get("start_hour", 0))
        except:
            raise ValidationError({'schedule': 'start_hour must be a integer'})
        try:
            start_minute = int(self.request.GET.get("start_minute", 0))
        except:
            raise ValidationError({'schedule': 'start_minute must be a integer'})

        try:
            end_day_of_week = int(self.request.GET.get("end_day_of_week", 6))
        except:
            raise ValidationError({'schedule': 'end_day_of_week must be a integer'})
        try:
            end_hour = int(self.request.GET.get("end_hour", 23))
        except:
            raise ValidationError({'schedule': 'end_hour must be a integer'})
        try:
            end_minute = int(self.request.GET.get("end_minute", 59))
        except:
            raise ValidationError({'schedule': 'end_minute must be a integer'})

        schedule_start = Slot.DEAFULT_INIT_DATE + datetime.timedelta(
            days=int(start_day_of_week), hours=int(start_hour), minutes=int(start_minute)
        )
        schedule_end = Slot.DEAFULT_INIT_DATE + datetime.timedelta(
            days=int(end_day_of_week), hours=int(end_hour), minutes=int(end_minute)
        )

        if(int(start_day_of_week) < 0 or int(start_day_of_week) > 6):
            raise ValidationError({"schedule": "start_day_of_week must be between 0 and 6"})

        if(int(end_day_of_week) < 0 or int(end_day_of_week) > 6):
            raise ValidationError({"schedule": "end_day_of_week must be between 0 and 6"})

        if(int(start_hour) < 0 or int(start_hour) > 23):
            raise ValidationError({"schedule": "start_hour must be between 0 and 23"})

        if(int(end_hour) < 0 or int(end_hour) > 23):
            raise ValidationError({"schedule": "end_hour must be between 0 and 23"})

        if(int(start_minute) < 0 or int(start_minute) > 59):
            raise ValidationError({"schedule": "start_minute must be between 0 and 59"})

        if(int(end_minute) < 0 or int(end_minute) > 59):
            raise ValidationError({"schedule": "end_minute must be between 0 and 59"})
        
        if(schedule_start > schedule_end):
            raise ValidationError({"schedule": "Start date cannot be after end date"})

        return queryset.filter(Q(schedule_start__gte=schedule_start), Q(schedule_end__lte=schedule_end))
