
from uuid import UUID
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from django.db.models import Q

from vbb_backend.program.api.serializers.slot import (
    MinimalSlotSerializer,
    SlotSerializer,
)
from vbb_backend.program.api.serializers.program import MinimalProgramSerializer
from vbb_backend.program.models import Computer, Slot
from vbb_backend.users.models import UserTypeEnum

from vbb_backend.session.tasks import create_session


# class SlotViewSet(ModelViewSet):
#     queryset = Slot.objects.all()
#     permission_classes = [IsAuthenticated]
#     serializer_class = SlotSerializer
#     lookup_field = "external_id"

#     def get_queryset(self):
#         queryset = self.queryset
#         user = self.request.user
#         computer = Computer.objects.get(external_id=self.kwargs.get("computer_external_id"))

#         queryset = queryset.filter(computer=computer)
#         if user.is_superuser:
#             pass
#         elif user.user_type in [UserTypeEnum.HEADMASTER.value]:
#             queryset = queryset.filter(computer__program__program_director=user)
#         else:
#             raise PermissionDenied()
#         return queryset

#     def get_computer(self):
#         return get_object_or_404(Computer, external_id=self.kwargs.get("computer_external_id"))

#     def perform_create(self, serializer):
#         serializer.save(computer=self.get_computer())


class SlotFilterSet(filters.FilterSet):
    computer = filters.UUIDFilter(field_name="computer__external_id")
    program = filters.UUIDFilter(field_name="computer__program__external_id")
    max_students = filters.NumberFilter(field_name="max_students", lookup_expr="lte")
    language = filters.CharFilter(field_name="language")
    is_mentor_assigned = filters.BooleanFilter(field_name="is_mentor_assigned")
    is_student_assigned = filters.BooleanFilter(field_name="is_student_assigned")


class SlotViewSet(ModelViewSet):
    queryset = Slot.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "external_id"
    filterset_class = SlotFilterSet
    serializer_class = MinimalSlotSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "list":
            return MinimalSlotSerializer
        return SlotSerializer

    def _check_min_max(self, field, value, min_value, max_value):
        if int(value) < min_value or int(value) > max_value:
            raise ValidationError(
                {"schedule": f"{field} must be between {min_value} and {max_value}"}
            )

    def get_allowed_queryset(self):
        queryset = self.queryset
        user = self.request.user

        queryset = queryset.filter(external_id=self.kwargs.get("external_id"))
        if user.is_superuser:
            pass
        elif user.user_type in [UserTypeEnum.HEADMASTER.value]:
            queryset = queryset.filter(computer__program__program_director=user)
        else:
            raise PermissionDenied()
        return queryset

    def get_queryset(self):
        queryset = self.queryset

        if self.action != "list":
            queryset = self.get_allowed_queryset()

        start_day_of_week = self.request.GET.get("start_day_of_week", 0)
        start_hour = self.request.GET.get("start_hour", 0)
        start_minute = self.request.GET.get("start_minute", 0)

        end_day_of_week = self.request.GET.get("end_day_of_week", 6)
        end_hour = self.request.GET.get("end_hour", 23)
        end_minute = self.request.GET.get("end_minute", 59)

        schedule_start = Slot.get_slot_time(start_day_of_week, start_hour, start_minute)
        schedule_end = Slot.get_slot_time(end_day_of_week, end_hour, end_minute)

        self._check_min_max("start_day_of_week", start_day_of_week, 0, 6)
        self._check_min_max("end_day_of_week", end_day_of_week, 0, 6)
        self._check_min_max("start_hour", start_hour, 0, 23)
        self._check_min_max("end_hour", end_hour, 0, 23)
        self._check_min_max("start_minute", start_minute, 0, 60)
        self._check_min_max("end_minute", end_minute, 0, 60)

        if schedule_start > schedule_end:
            raise ValidationError({"schedule": "Start date cannot be after end date"})

        return queryset.filter(
            Q(schedule_start__gte=schedule_start), Q(schedule_end__lte=schedule_end)
        )

    def check_if_uuid(self, uuid_to_test):
        try:
            uuid_obj = UUID(uuid_to_test)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test

    def get_computer(self, computer_id):
        return get_object_or_404(Computer, external_id=computer_id)

    def perform_create(self, serializer):
        computer_id = self.request.data.get("computer_external_id")
        if not computer_id:
            raise ValidationError({"message": "computer id required"})
        if not self.check_if_uuid(computer_id):
            raise ValidationError({"message": "computer id must be valid UUID"})

        serializer.save(computer=self.get_computer(computer_id))

    def perform_create(self, serializer):
        slot = serializer.save()
        create_session.apply_async((slot.pk,), countdown=5)

    @action(methods=["GET"], detail=False)
    def get_unique_programs(self, request):
        qs = self.queryset.select_related("computer", "computer__program").distinct(
            "computer__program"
        )

        programs = [slot.computer.program for slot in qs]
        data = MinimalProgramSerializer(programs, many=True)
        return Response(data.data)
