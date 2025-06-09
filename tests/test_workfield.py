from odoo.tests import TransactionCase

class TestWorkfield(TransactionCase):

    @classmethod
    def setUpClass(cls): 
        super().setUpClass()



    def test_create_workfield(self):
        workfield=self.env["appointment.workfield"].create(
            {
                "name":"Test Workfield",
            }
        )

        self.assertIsNotNone(workfield)
        self.assertEqual(workfield.name, 'Test Workfield')
        self.assertFalse(workfield.service_ids)
        self.assertFalse(workfield.employee_ids)
        
    def test_unique_name(self):
        self.env['appointment.workfield'].create({"name": "Unique Workfield"})
        with self.assertRaises(Exception):
            self.env['appointment.workfield'].create({"name": "Unique Workfield"})


    
    def test_workfield_rel(self):
        workfield=self.env["appointment.workfield"].create({
            "name":"Test Workfield"
        })


        service=self.env["appointment.service"].create(
            {
                "name":"Test Service",
                "price":1200.0,
                "workfield_id":workfield.id,
            })

        employee=self.env["appointment.employee"].create(
            {
                "name":"Test Employee",
                "workfield_id":workfield.id,
            })

        self.assertIn(service,workfield.service_ids)
        self.assertIn(employee,workfield.employee_ids)