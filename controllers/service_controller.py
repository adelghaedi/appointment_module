from odoo.http import Controller,route,request


class ServiceController(Controller):
    @route("/service" , auth="user",type="http",website=True)
    


    def render_service_list(self):
        services = request.env['appointment.service'].sudo().search([])
        return request.render(
            "appointment_module.appointment_service_list_template",{
                'services':services
            }
        )

    

