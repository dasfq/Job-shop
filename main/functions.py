def get_parametrs_list(self):
    param_list = []
    parameter = {
        'name': '',
        'value': '',
        'units': '',
    }
    for param in self.object.parameter.all():
        parameter['name'] = param.parameter.name
        parameter['value'] = param.value
        parameter['units'] = param.parameter.units
        param_list.append(parameter)
    return