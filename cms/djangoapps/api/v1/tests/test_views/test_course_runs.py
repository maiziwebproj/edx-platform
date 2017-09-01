from django.core.urlresolvers import reverse

from student.tests.factories import AdminFactory, TEST_PASSWORD, UserFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory
from ...serializers.course_runs import CourseRunSerializer


class CourseRunViewSetTests(ModuleStoreTestCase):
    maxDiff = None
    list_url = reverse('api:v1:course_run-list')

    def test_list_without_authentication(self):
        response = self.client.get(self.list_url)
        assert response.status_code == 401

    def test_list_without_authorization(self):
        user = UserFactory(is_staff=False)
        self.client.login(username=user.username, password=TEST_PASSWORD)
        response = self.client.get(self.list_url)
        assert response.status_code == 403

    def test_list_results(self):
        course_runs = CourseFactory.create_batch(3)
        user = AdminFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        response = self.client.get(self.list_url)
        assert response.status_code == 200

        # Order matters for the assertion
        course_runs = sorted(course_runs, key=lambda course_run: str(course_run.id))
        actual = sorted(response.data, key=lambda course_run: course_run['id'])
        assert actual == CourseRunSerializer(course_runs, many=True).data

    def test_retrieve(self):
        user = AdminFactory()
        self.client.login(username=user.username, password=TEST_PASSWORD)
        course_run = CourseFactory()
        url = reverse('api:v1:course_run-detail', kwargs={'pk': str(course_run.id)})
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data == CourseRunSerializer(course_run).data
