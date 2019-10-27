import random

def data_magic(data_dict):
    if 'voltage_AB' in data_dict.keys():
        data_dict['voltage_AB'] = round(random.random()*4, 2)+558
    if 'voltage_BC' in data_dict.keys():
        data_dict['voltage_BC'] = round(random.random()*4, 2)+558
    if 'voltage_CA' in data_dict.keys():
        data_dict['voltage_CA'] = round(random.random()*4, 2)+558
    return data_dict