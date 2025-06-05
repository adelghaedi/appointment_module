{
    "name": "Appointment",
    "summary": "Manage services, customers, and appointments",
    "version": "17.0.1.0.0",
    "description":"",
    "category": "Sales",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "base",
        "website",
        "hr",
    ],
    "data":[
        "security/group.xml",
        "security/ir.model.access.csv",
        "security/appointment_security.xml",
        "views/customer_view.xml",
        "views/employee_view.xml",
        "views/appointment_view.xml",
        "views/service_view.xml",
        "views/workfield_view.xml",
        "views/main_view.xml",
        "templates/service_list_template.xml",
        "templates/service_detail_template.xml",
        "templates/appointment_report_template.xml",
    ],
    "controllers":[
        "controllers/service_controller.py",
    ]
}
