from odoo import models,fields,api




class Service(models.Model):
    _name="appointment.service"
    _inherit=["mail.thread"]
    _sql_constraints=[
        ("_check_unique_name","UNIQUE(name)","This service exists..."),
        ("_check_price_positive","CHECK(price>0)","Price must be positive..."),
        ("_check_quantity_nonnegative","CHECK(quantity>=0)","Quantity cannot negative..."),
    ]
    _order="quantity desc"

    name=fields.Char(string="Name",required=True,tracking=True)
    price=fields.Float(string="Price",required=True,tracking=True)
    image=fields.Image(string="Image")
    sequence=fields.Integer(string="Sequence",default=10)
    quantity=fields.Integer(string="Quantity",tracking=True)

    workfield_id=fields.Many2one(
        "appointment.workfield",
        string="WorkField",
        ondelete="cascade"
        )
    
    employee_ids=fields.Many2many(
        "hr.employee",
        string="Employees",
        relation="appointment_employee_service_rel",
        column1="service_ids",
        column2="employee_ids",
    )    



    def action_service_website(self):
        self.ensure_one()
        service_id=self.id
        return {    
                "type": "ir.actions.act_url",
                "url": f"http://localhost:8069/service/{service_id}",
                "target": "self",
        }

    def action_post_message(self):
        self.message_post(body=f"Hi, Welcome to {self.name} Service...")


    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'name' in init_values:
            return self.env.ref('appointment_module.service_name_change')
        if "price" in init_values:
            return self.env.ref("appointment_module.service_price_change")
        if "quantity" in init_values:
            return self.env.ref("appointment_module.service_quantity_change")

        return super()._track_subtype(init_values)


    

    


    
