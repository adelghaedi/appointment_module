from odoo import models,fields,api


class Customer(models.Model):
    _name="appointment.customer"
    _inherit="appointment.person"

   


    appointment_ids=fields.One2many(
        "appointment.appointment",
        inverse_name="customer_id",
        string="Appointments",
    )

    


    @api.depends("appointment_ids")
    def _compute_total_appointments(self):
        for record in self:
            record.total_appointments=len(record.appointment_ids)

    def action_show_appointment(self)->dict:
        self.ensure_one()
        return {
            "type":"ir.actions.act_window",
            "name":"Appointments",
            "view_mode":"tree,form",
            "res_model":"appointment.appointment",
            "domain": [("customer_id", "=", self.id)],
            "context": {"default_customer_id": self.id},
            "target": "current",
        }
