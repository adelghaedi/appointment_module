from odoo import models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self, vals_list):
        users = super().create(vals_list)
        employee_group = self.env.ref('appointment_module.group_employee')
        for user in users:
            employee = self.env['hr.employee'].search(
                [('user_id', '=', user.id)], limit=1)
            if employee and employee_group not in user.groups_id:
                user.write({'groups_id': [(4, employee_group.id)]})
        return users
