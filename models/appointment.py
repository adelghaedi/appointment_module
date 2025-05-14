from odoo import models,fields,api
from odoo.exceptions import ValidationError
from datetime import timedelta


class Appointment(models.Model):
    _name="appointment.appointment"
    _sql_constraints=[
        ("_check_duration_positive","CHECK(duration>0)","Duration must be positive.")
    ]

    start_datetime=fields.Datetime(string="start_datetime",required=True)
    duration=fields.Float(string="duraton",default="1.0",required=True)
    end_datetime=fields.Datetime(string="end_datetime",compute="_compute_end_datetime",store=True)



    service_id =fields.Many2one(
        "appointment.service",
        string="Service",
        ondelete="restrict",
        # domain="[('employee_ids','in',employee_id)]"
    )

    customer_id=fields.Many2one(
        "appointment.customer",
        string="Customer",
        ondelete="restrict",
    )

    employee_id=fields.Many2one(
        "appointment.employee",
        string="Employee",
        ondelete="restrict",
        domain="[('service_ids', 'in', service_id)]"
    )


    @api.depends("start_datetime" , "duration")
    def _compute_end_datetime(self)->None:
        for record in self:
            if record.start_datetime and record.duration:
                record.end_datetime=record.start_datetime + timedelta(hours=record.duration)
            else:
                record.end_datetime=False

    @api.constrains("start_datetime")
    def _check_start_datetime_by_now(self):
        for record in self:
            if record.start_datetime<fields.Datetime.now():
                raise ValidationError("The start datetime cannot be set in the past")
            


    @api.constrains("customer_id","start_datetime","end_datetime")
    def _check_unique_customer_appointment_date_time(self):
        for record in self:
            if not (record.customer_id and record.start_datetime and record.end_datetime):
                continue

            conflict=self.search([
                  ('id', '!=', record.id),
                  ('customer_id', '=', record.customer_id.id),
                   ('start_datetime', '<', record.end_datetime),
                   ('end_datetime', '>', record.start_datetime),
            ])

            if conflict:
                raise ValidationError("The end datetime conflicts with another appointment.")

    

    @api.constrains("employee_id","start_datetime","end_datetime")
    def _check_unique_employee_appointment_date_time(self):
        for record in self:
            if not (record.employee_id and record.start_datetime and record.end_datetime):
                continue

            conflict=self.search([
                  ('id', '!=', record.id),
                  ('employee_id', '=', record.employee_id.id),
                   ('start_datetime', '<', record.end_datetime),
                   ('end_datetime', '>', record.start_datetime),
            ])

            if conflict:
                raise ValidationError("The end datetime conflicts with another appointment.")