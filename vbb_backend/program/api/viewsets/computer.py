from re import IGNORECASE
import django
from django.db.models.fields import DateField
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from vbb_backend.program.api.serializers.computer import ComputerSerializer
from vbb_backend.program.models import Program, Computer
from vbb_backend.users.models import UserTypeEnum


class ComputerViewSet(ModelViewSet):
    queryset = Computer.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = ComputerSerializer
    lookup_field = "external_id"

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        program = Program.objects.get(
            external_id=self.kwargs.get("program_external_id")
        )
        queryset = queryset.filter(program=program)
        if user.is_superuser:
            pass
        elif user.user_type in [UserTypeEnum.HEADMASTER.value]:
            queryset = queryset.filter(program__program_director=user)
        else:
            raise PermissionDenied()
        return queryset

    def get_program(self):
        return get_object_or_404(
            Program, external_id=self.kwargs.get("program_external_id")
        )

    def perform_create(self, serializer):
        serializer.save(program=self.get_program())
