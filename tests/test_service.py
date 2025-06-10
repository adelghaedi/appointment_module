from odoo.tests import TransactionCase

class TestService(TransactionCase):

    @classmethod
    def setUpClass(cls): 
        super().setUpClass()



    def test_create_service(self):
        service=self.env["appointment.service"].create(
            {
                "name":"Test Service",
                "price":1000.0,
            }
        )

        self.assertIsNotNone(service)
        self.assertEqual(service.name, 'Test Service')
        self.assertEqual(service.quantity,0)
        self.assertEqual(service.sequence,10)
        self.assertGreater(service.price, 0)
        self.assertFalse(service.image)
        self.assertFalse(service.workfield_id)
        self.assertFalse(service.employee_ids)
    
    def test_unique_name(self):
        self.env["appointment.service"].create(
            {
                "name":"Unique Service",
                "price":5000.0,
            })
        with self.assertRaises(Exception):
            self.env["appointment.service"].create(
                {
                    "name":"Unique Service",
                    "price":3000.0,
                })

        