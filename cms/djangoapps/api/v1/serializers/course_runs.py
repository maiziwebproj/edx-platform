from rest_framework import serializers

from student.models import CourseAccessRole


class CourseAccessRoleSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = CourseAccessRole
        fields = ('user', 'role',)


class CourseRunScheduleSerializer(serializers.Serializer):
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    enrollment_start = serializers.DateTimeField()
    enrollment_end = serializers.DateTimeField()


class CourseRunSerializer(serializers.Serializer):
    id = serializers.CharField()
    schedule = CourseRunScheduleSerializer(source='*')
    team = serializers.SerializerMethodField()

    def get_team(self, course_run):
        roles = CourseAccessRole.objects.filter(course_id=course_run.id)
        return CourseAccessRoleSerializer(roles, many=True).data
