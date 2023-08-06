from djangoautoconf.auto_conf_admin_tools.admin_register import AdminRegister
from . import models


AdminRegister().register_all_model(models)
