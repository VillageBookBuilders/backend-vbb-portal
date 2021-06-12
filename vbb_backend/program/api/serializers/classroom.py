from rest_framework import serializers

from vbb_backend.program.api.serializers.school import SchoolSerializer
from vbb_backend.program.models import Classroom, School
from vbb_backend.utils.serializer.external_id_serializer import (
    ExternalIdSerializerField,
)


class ClassroomSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)

    school_object = SchoolSerializer(source="program", read_only=True)

    school = ExternalIdSerializerField(queryset=School.objects.all(), required=False)

    class Meta:
        model = Classroom
        exclude = ("deleted", "external_id")
