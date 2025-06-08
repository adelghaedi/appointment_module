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
        