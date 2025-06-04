from odoo import models,fields,api
from odoo.exceptions import ValidationError,UserError
from datetime import timedelta


class Appointment(models.Model):
    _name="appointment.appointment"
    _sql_constraints=[
        ("_check_duration_positive","CHECK(duration>0)","Duration must be positive.")
    ]

    start_datetime=fields.Datetime(string="start_datetime",required=True)
    duration=fields.Float(string="duraton",default=1.0,required=True)
    end_datetime=fields.Datetime(string="end_datetime",compute="_compute_end_datetime",store=True)
    calendar_event_created = fields.Boolean(string='Calendar Event Created', default=False)



    service_id =fields.Many2one(
        "appointment.service",
        string="Service",
        ondelete="restrict",
    )

    customer_id=fields.Many2one(
        "res.partner",
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
    

    def create_calendar_event(self):
        for record in self:
            event_name= f"Appointment Event with {record.employee_id.name} Employee on {record.start_datetime}"
            
            if record.calendar_event_created:
                raise UserError(f"{event_name} has already been created")
            self.env['calendar.event'].create({
                'name': event_name,
                'start': record.start_datetime,
                'stop': record.end_datetime,
                'partner_ids': [(4, record.customer_id.id)],
            })
            record.calendar_event_created = True
    
    
        
    
  