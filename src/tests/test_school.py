from rest_framework.test import APITestCase
from school.models import School
from school.factories import (
    SchoolFactory,
    TeacherFactory,
    ClassRoomFactory,
    StudentFactory,
    StudentCardFactory,
)


class AccountTests(APITestCase):

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        school_1 = SchoolFactory()
        teacher_1 = TeacherFactory(school=school_1)
        classroom_1 = ClassRoomFactory(school=school_1, teacher=teacher_1)
        student_1 = StudentFactory(classroom=classroom_1)

        school_2 = SchoolFactory()
        teacher_2 = TeacherFactory(school=school_2)
        classroom_2 = ClassRoomFactory(school=school_2, teacher=teacher_2)
        student_2 = StudentFactory(classroom=classroom_2)
        print(School.objects.all())
        print('test_create_account')

        url = '/fairy/client/school/student/list/'
        response = self.client.post(
            url,
            format='json',
            data={
                'fairyspace': {
                    'fields': [
                        'id',
                        'name',
                        'classroom',
                        {
                            'school': [
                                'name',
                                {
                                    'teachers': {
                                        'name',
                                    },
                                },
                            ]
                        },
                    ],
                    # 'filters': [{'field': 'id', 'operator': '=', 'value': 1}],
                }
            },
        )

        print(response.data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 1)
