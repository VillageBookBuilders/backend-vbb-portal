from rest_framework import serializers

from vbb_backend.program.api.serializers.program import MinimalProgramSerializer
from vbb_backend.program.models import Program, School
from vbb_backend.utils.serializer.external_id_serializer import (
    ExternalIdSerializerField,
)


class SchoolSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)

    program_object = MinimalProgramSerializer(source="program", read_only=True)

    program = ExternalIdSerializerField(queryset=Program.objects.all(), required=False)

    class Meta:
        model = School
        exclude = ("deleted", "external_id")
