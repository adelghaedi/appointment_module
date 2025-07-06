from odoo.tests import TransactionCase


class TestService(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.employee = cls.env['hr.employee'].create({
            'name': 'Test Employee',
            'work_email': 'test.employee@example.com',
        })

        cls.employee_group = cls.env.ref('appointment_module.group_employee')

    def test_action_create_user(self):
        self.assertFalse(self.employee.user_id,
                         "Employee should not have a user before action_create_user")

        result = self.employee.action_create_user()

        self.assertTrue(self.employee.user_id,
                        "Employee should have a user after action_create_user")

        self.assertEqual(self.employee.user_id.name, self.employee.name,
                         "User name should match employee name")
        self.assertEqual(self.employee.user_id.login, self.employee.work_email,
                         "User login should match employee work_email")

        self.assertIn(
            self.employee_group.id,
            self.employee.user_id.groups_id.ids,
            "User should be in the Appointment Employee group"
        )
