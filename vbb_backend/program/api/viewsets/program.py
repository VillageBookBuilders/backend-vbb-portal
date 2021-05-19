from django.db.models import query
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from vbb_backend.program.api.serializers.program import ProgramSerializer
from vbb_backend.program.models import Program
from vbb_backend.users.models import UserTypeEnum


class ProgramViewSet(ModelViewSet):
    queryset = Program.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProgramSerializer
    lookup_field = "external_id"

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if user.is_superuser:
            pass
        elif user.user_type in [UserTypeEnum.HEADMASTER.value]:
            queryset = queryset.filter(program_director=user)
        else:
            raise PermissionDenied()
        return queryset
