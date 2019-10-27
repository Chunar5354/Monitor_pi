import random

def create_data(list_src):
    for sum_list in list_src:
        sum_list[1] = str(round(random.random()*10, 2)+555)
    return list_src

def data_magic(data_dict):
    if 'voltage_AB' in data_dict.keys():
        data_dict['voltage_AB'] = create_data(data_dict['voltage_AB'])
    if 'voltage_BC' in data_dict.keys():
        data_dict['voltage_BC'] = create_data(data_dict['voltage_BC'])
    if 'voltage_CA' in data_dict.keys():
        data_dict['voltage_CA'] = create_data(data_dict['voltage_CA'])
    return data_dict
