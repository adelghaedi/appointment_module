from odoo.exceptions import ValidationError
from odoo import models,fields,api


class Employee(models.Model):
    _name="appointment.employee"


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


    


    appointment_ids=fields.One2many(
        "appointment.appointment",
        inverse_name="employee_id",
        string="Appointments",
    )


    service_ids=fields.Many2many(
        "appointment.service",
        string="Services",
        relation="appointment_employee_service_rel",
        column1="employee_ids",
        column2="service_ids",
    )

    workfield_id=fields.Many2one(
        "appointment.workfield",
        string="WorkField"
    )

    @api.depends("appointment_ids")
    def _compute_total_appointments(self)->None:
        for record in self:
            record.total_appointments=len(record.appointment_ids)


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
    


    # create action and return it
    def action_show_appointment(self) :
        self.ensure_one()
        return {
            "type":"ir.actions.act_window",
            "name":"Appointments",
            "view_mode":"tree,form",
            "res_model":"appointment.appointment",
            "domain": [("employee_id", "=", self.id)],
            "context": {"default_employee_id": self.id},
            "target": "current",
        }
    
    # return defulat action 
    def action_show_customers(self):
        return self.env.ref("appointment_module.appointment_customer_action").read()[0]


    # change view 
    def action_set_name(self):
        for record in self:
            record.name="name"