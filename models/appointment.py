from odoo import models,fields,api
from odoo.exceptions import ValidationError
from datetime import timedelta


class Appointment(models.Model):
    _name="appointment.appointment"
    _sql_constraints=[
        ("_check_duration_positive","CHECK(duration>0)","Duration must be positive.")
    ]

    start_datetime=fields.Datetime(string="start_datetime",required=True)
    duration=fields.Float(string="duraton",default=1.0,required=True)
    end_datetime=fields.Datetime(string="end_datetime",compute="_compute_end_datetime",store=True)
    state=fields.Selection(
        [
        ("draft","Draft"),
         ("confirmed","Confirmed"),
         ("rejected","Rejected"),
        ],
        string="state",
        default="draft",
        tracking=True,
    )



    service_id =fields.Many2one(
        "appointment.service",
        string="Service",
        ondelete="restrict",
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

    @api.constrains("service_id")
    def _check_quantity_selected_service(self):
        for record in self:
            if record.service_id and record.service_id.quantity<=0:
                raise ValidationError("No available quantity for the selected service.")
    
    @api.model
    def create(self,vals):
        record=super().create(vals)
        service=record.service_id
        if service and service.quantity:
            service.quantity-=1
        return record
    
    def _check_employee_user(self):
        if not self.env.user.has_group('appointment.group_employee'):
            raise ValidationError("Only employees can perform this action.")

    def action_confirm(self):
        if self.start_datetime>fields.Datetime.now():
            self.write({"state":"confirmed"})
        else:
            raise ValidationError("Cannot confirm an appointment that has already passed.")

    def action_reject(self):
        if self.start_datetime > fields.Datetime.now():
            self.write({"state":"rejected"})
        else:
            raise ValidationError("Cannot confirm an appointment that has already passed.")

    def action_done(self):
        self._check_employee_user()
        self.write({'state': 'done'})

    def action_show(self):
        return {
            'type': 'ir.actions.act_window.message',
            'title': 'Show Action',
            'message': 'This is the Show button!',
        }
    
