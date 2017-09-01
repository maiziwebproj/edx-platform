import datetime

import pytz

from student.roles import CourseInstructorRole, CourseStaffRole
from student.tests.factories import UserFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory
from ...serializers.course_runs import CourseRunSerializer


class CourseRunSerializerTests(ModuleStoreTestCase):
    def serialize_datetime(self, d):
        return d.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    def test_data(self):
        start = datetime.datetime.now(pytz.UTC)
        end = start + datetime.timedelta(days=30)
        enrollment_start = start - datetime.timedelta(days=7)
        enrollment_end = end - datetime.timedelta(days=14)

        course = CourseFactory(start=start, end=end, enrollment_start=enrollment_start, enrollment_end=enrollment_end)
        instructor = UserFactory()
        CourseInstructorRole(course.id).add_users(instructor)
        staff = UserFactory()
        CourseStaffRole(course.id).add_users(staff)

        serializer = CourseRunSerializer(course)
        expected = {
            'id': str(course.id),
            'schedule': {
                'start': self.serialize_datetime(start),
                'end': self.serialize_datetime(end),
                'enrollment_start': self.serialize_datetime(enrollment_start),
                'enrollment_end': self.serialize_datetime(enrollment_end),
            },
            'team': [
                {
                    'user': instructor.username,
                    'role': 'instructor',
                },
                {
                    'user': staff.username,
                    'role': 'staff',
                },
            ],
        }
        assert serializer.data == expected
