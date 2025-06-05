from odoo import models,fields,api
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _inherit="hr.employee"

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


    @api.model
    def create(self, vals):
        if not vals.get('user_id'):
            user_model = self.env['res.users']
            user_vals = {

                'name': vals.get('name'),
                'login': vals.get('work_email') or vals.get('personal_email') or vals.get('name').replace(' ', '').lower(),
                'password': '12345',
            }
            if vals.get('image_1920'):
                user_vals['image_1920'] = vals.get('image_1920')
            
            user = user_model.create(user_vals)
            vals['user_id'] = user.id

        employee = super(Employee, self).create(vals)

        group_employee = self.env.ref('appointment_module.group_employee')
        if employee.user_id and group_employee:
            employee.user_id.write({'groups_id': [(4, group_employee.id)]})
        
        return employee
    


    def write(self,vals):

        user_fields={}

        if "name" in vals:
            user_fields["name"]=vals["name"]
        if "image_1920" in vals:
            user_fields["image_1920"]=vals["image_1920"]
        login=vals.get("work_email") or vals.get("personal_email") or vals.get("name")
        print(login)
        if login:
            user_fields["login"]=login
        
        result=super(Employee,self).write(vals)

        for employee in self:
            if employee.user_id and user_fields:
                employee.user_id.with_context(skip_employee_sync=True).write(user_fields)
                print("ok")



        return result
    
    
    
    # @api.ondelete(at_uninstall=False)
    # def unlink(self):
    #     for employee in self:
    #         user=employee.user_id
    #         employee.user_id=False
    #         if user:
    #             user.unlink()
    #     return super().unlink()

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
            "target": "current",
        }
    
    # return defulat action 
    def action_show_customers(self):
        return self.env.ref("appointment_module.appointment_customer_action").read()[0]


    # change view 
    def action_set_name(self):
        for record in self:
            record.name="name"