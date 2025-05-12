from odoo import models,fields,api

class Service(models.Model):
    _name="appointment.service"
    _sql_constraints=[
        ("_check_unique_name","UNIQUE(name)","This servie exists..."),
        ("_check_price_positive","CHECK(price>0)","Price must be positive..."),
    ]

    name=fields.Char(string="name",required=True)
    price=fields.Float(string="price",required=True)

    workfield_id=fields.Many2one(
        "appointment.workfield",
        string="WorkField",
        ondelete="cascade"
        )
    


    