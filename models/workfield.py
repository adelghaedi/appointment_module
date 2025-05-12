from odoo import models,fields,api

class WorkField(models.Model):
    _name="appointment.workfield"
    _sql_constraints=[
        ("_check_unique_name","UNIQUE(name)","This workfield exists..."),
    ]

    name=fields.Char(string="name",required=True)

    service_ids=fields.One2many(
        "appointment.service",
        inverse_name="workfield_id",
        string="Servicers"
    )

    employee_ids=fields.One2many(
        "appointment.employee",
        inverse_name="workfield_id",
        string="Employees",
    )