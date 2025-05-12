from odoo import models,fields,api


class Employee(models.Model):
    _name="appointment.employee"
    _inherit="appointment.person"
    


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
            "target": "new",
        }
    
    # return defulat action 
    def action_show_customers(self):
        return self.env.ref("appointment_module.appointment_customer_action").read()[0]


    # change view 
    def action_set_name(self):
        for record in self:
            record.name="name"