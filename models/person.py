from odoo.exceptions import ValidationError
from odoo import models,fields,api


class Customer(models.AbstractModel):
    _name="appointment.person"

    name=fields.Char(string="name",required=True)
    phone = fields.Char(string="phone_number")
    email = fields.Char(string="email")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown')
    ], string="gender", default='unknown')
    birth_date = fields.Date(string="birth_date")
    image=fields.Image(string="customer_image")
    total_appointments=fields.Integer(compute="_compute_total_appointments")


    @api.constrains("email")
    def _check_correct_email(self):
        for record in self:
            if record.email:
                if "@" not in record.email:
                    raise ValidationError("email must be contains @ sign...")



    @api.constrains("phone")
    def _check_correct_phone(self):
        for record in self:
            if record.phone:
                if not record.phone.isnumeric():
                    raise ValidationError("phone must be digits...")
                if not record.phone.startswith("0"):
                    raise ValidationError("phone must be start with zero digit...")
                if  len(record.phone)!=11:
                    raise ValidationError("phone must be eleven digits...")


                
