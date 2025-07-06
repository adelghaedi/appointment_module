from odoo.tests import TransactionCase


class TestService(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        self.employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
            'work_email': 'test.employee@example.com',
        })

        self.employee_group = self.env.ref('appointment_module.group_employee')

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

        # self.assertEqual(result['type'], 'ir.actions.act_window', "Action should return an act_window")
        # self.assertEqual(result['res_model'], 'res.users', "Action should target res.users model")
        # self.assertEqual(result['res_id'], self.employee.user_id.id, "Action should target the created user")
