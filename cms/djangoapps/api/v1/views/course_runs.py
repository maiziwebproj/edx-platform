from edx_rest_framework_extensions.authentication import JwtAuthentication
from opaque_keys.edx.keys import CourseKey
from rest_framework import permissions, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from contentstore.views.course import _accessible_courses_iter, get_course_and_check_access
from ..serializers.course_runs import CourseRunSerializer


class CourseRunViewSet(viewsets.ViewSet):
    authentication_classes = (JwtAuthentication, SessionAuthentication,)
    # TODO Consolidate with setting in LMS
    lookup_value_regex = r'[^/+]+(/|\+)[^/+]+(/|\+)[^/]+'  # settings.COURSE_KEY_REGEX
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = CourseRunSerializer

    def list(self, request):
        course_runs, __ = _accessible_courses_iter(request)
        serializer = self.serializer_class(course_runs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        course_run_key = CourseKey.from_string(pk)
        course_run = get_course_and_check_access(course_run_key, request.user)
        serializer = self.serializer_class(course_run)
        return Response(serializer.data)

    def update(self, request, pk=None):
        raise NotImplementedError
