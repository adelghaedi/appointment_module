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

    name=fields.Char(string="name",required=True,tracking=True)
    price=fields.Float(string="price",required=True,tracking=True)
    image=fields.Image(string="service_image")
    sequence=fields.Integer(string="sequence",default=10)
    quantity=fields.Integer(string="quantity",tracking=True)

    workfield_id=fields.Many2one(
        "appointment.workfield",
        string="WorkField",
        ondelete="cascade"
        )
    
    employee_ids=fields.Many2many(
        "appointment.employee",
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


    

    


    
