from odoo import models,fields,api




class Service(models.Model):
    _name="appointment.service"
    _sql_constraints=[
        ("_check_unique_name","UNIQUE(name)","This service exists..."),
        ("_check_price_positive","CHECK(price>0)","Price must be positive..."),
        ("_check_quantity_nonnegative","CHECK(quantity>=0)","Quantity cannot negative..."),
    ]
    _order="quantity desc"

    name=fields.Char(string="name",required=True)
    price=fields.Float(string="price",required=True)
    image=fields.Image(string="service_image")
    sequence=fields.Integer(string="sequence",default=10)
    quantity=fields.Integer(string="quantity")

    workfield_id=fields.Many2one(
        "appointment.workfield",
        string="WorkField",
        ondelete="cascade"
        )
    
<<<<<<< HEAD
=======
    employee_ids=fields.Many2many(
        "appointment.employee",
        string="Employees",
        relation="appointment_employee_service_rel",
        column1="service_ids",
        column2="employee_ids",
    )    


    
>>>>>>> 17.0
