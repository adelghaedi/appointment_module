from odoo.tests import TransactionCase

class TestService(TransactionCase):

    @staticmethod
    def setUpClass(cls): 
        super().setUpClass()

        # cls.workfield=cls.env["appointment.workfield"].create(
        #    {name:"Test Workfield",})


    def test_create_service(self):
        service=self.env["appointment.service"].create(
            {
                name:"Test Service",
                price:1000.0,
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