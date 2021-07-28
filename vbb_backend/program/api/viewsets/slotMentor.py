from uuid import UUID
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from vbb_backend.program.api.serializers.slotMentor import (
    MentorSlotBookingSerializer,
    MentorSlotSerializer,
)
from vbb_backend.program.models import Slot, MentorSlotAssociation
from vbb_backend.users.models import UserTypeEnum, Mentor


class MentorSlotViewSet(ModelViewSet):
    queryset = MentorSlotAssociation.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MentorSlotSerializer
    lookup_field = "external_id"

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        slot = Slot.objects.get(external_id=self.kwargs.get("slot_external_id"))
        queryset = queryset.filter(slot=slot)
        if user.is_superuser:
            pass
        elif user.user_type in [UserTypeEnum.HEADMASTER.value]:
            queryset = queryset.filter(slot__computer__program__program_director=user)
        else:
            raise PermissionDenied()
        return queryset

    def check_if_uuid(self, uuid_to_test):
        try:
            uuid_obj = UUID(uuid_to_test)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test

    def get_slot(self):
        return get_object_or_404(
            Slot, external_id=self.kwargs.get("slot_external_id")
        )

    def get_mentor(self):
        return get_object_or_404(
            Mentor, external_id=self.request.data.get("mentor")
        )

    def perform_create(self, serializer):
        mentor_id = self.request.data.get("mentor")
        if not mentor_id:
            raise ValidationError({"message": "mentor id required"})
        if not self.check_if_uuid(mentor_id):
            raise ValidationError({"message": "mentor id must be valid UUID"})

        serializer.save(slot=self.get_slot(), mentor=self.get_mentor())


class MentorBookingViewSet(ModelViewSet):
    queryset = MentorSlotAssociation.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MentorSlotBookingSerializer
    lookup_field = "external_id"

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        slot = Slot.objects.get(external_id=self.kwargs.get("slot_external_id"))
        queryset = queryset.filter(slot=slot)
        if user.is_superuser:
            pass
        elif user.user_type in [UserTypeEnum.MENTOR.value]:
            queryset = queryset.filter(mentor=user)
        else:
            raise PermissionDenied()
        return queryset

    def get_slot(self):
        return get_object_or_404(
            Slot.objects.all(), external_id=self.kwargs.get("slot_external_id")
        )

    def perform_create(self, serializer):
        serializer.save(slot=self.get_slot())
