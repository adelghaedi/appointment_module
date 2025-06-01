from odoo.http import Controller,route,request


class ServiceListController(Controller):
    @route("/service" , auth="user",type="http",website=True)
    


    def render_service_list(self):
        services = request.env['appointment.service'].sudo().search([])
        return request.render(
            "appointment_module.appointment_service_list_template",{
                'services':services
            }
        )


class ServiceDetailController(Controller):
    @route('/service/<int:service_id>',type="http",auth="user",website=True)



    def render_service(self,service_id):
        service=request.env["appointment.service"].sudo().browse(service_id)

        if not service.exists():
            return request.not_found()
        else:
            return request.render('appointment_module.appointment_service_detail_template',{
                "service":service,
            }
            )


    

