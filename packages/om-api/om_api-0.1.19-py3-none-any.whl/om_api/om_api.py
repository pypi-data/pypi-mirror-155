import json
import requests
import pandas as pd

def make_request(request_type: str, url: str, cookie: dict, param: dict = ..., data: dict = ...):
    if param is ...:
        param = {}
    if data is ...:
        data = {}
    if request_type == 'get':
        response = requests.get(url, cookies=cookie, params=param)
    else:
        response = requests.post(url, cookies=cookie, params=param, data=data)

    id = str(response.json()["params"]["id"])
    responseToken = str(response.json()["params"]["responseToken"])
    monitoring_url = url+'/status/'+ id
    response = requests.get(monitoring_url, cookies=cookie)


    while response.json()['params']['status'] != 'SUCCESS':
        response = requests.get(monitoring_url, cookies=cookie)
        if response.json()['params']['status'] in ['FAILED', 'TIMED_OUT', 'REJECTED', 'REMOVED', 'CANCELED']:
            print('Request failed')
            break

    print(response.json()['params']['status'])
    
    response = requests.get(f'{url}/response/{id}?responseToken={responseToken}', cookies=cookie)
    return response


def DataFrame_to_List(data):
    list = []
    list.append(data.columns.to_list())
    list.append(data.values.tolist())
    return list


def get_properties(list_name: str, url: str, cookie: dict, view_name: str= ...):
    """Возвращает список свойств справочника"""
    if view_name == ...:
        param = {"type": "list", # Тип источника multicube | om_multicube | list
            "name": list_name  # Название МК/справочника
            }
    else:
        param = {"type": "list", # Тип источника multicube | om_multicube | list
            "name": list_name,  # Название МК/справочника
            'view_name' : view_name,
            }
    response = make_request(url=url, request_type='get', cookie=cookie, param=param)
    row_data = response.json()['params']['data']['requestedData']
    return row_data[0][6:] #Корректно для пользователя с правами администратора воркспейса

def get_list(list_name: str, url: str, cookie: dict):
    """Возвращает справочник в формате DataFrame"""
    param = {"type": "list", # Тип источника multicube | om_multicube | list
         "name": list_name  # Название МК/справочника
        }
    response = make_request(url=url, cookie=cookie, request_type= 'get', param=param)
    row_data = response.json()['params']['data']['requestedData']
    data = pd.DataFrame(row_data[1:],
                        columns=row_data[0])
    return data


def get_parents(list_name: str, url: str, cookie: dict, parent: str = ...):
    """Возвращает список парентов в справочнике"""
    data = get_list(list_name, url, cookie)
    lists = data['List'].unique()
    ierarhy = {}
    lvl = len(lists)
    for i in lists:
        ierarhy.update({lvl:i})
        lvl -= 1
    if len(lists) == 1:
        data = data.query(f'Parent.isna()')
    else:
        if parent == ...:
            data = data.query(f'List == \'{ierarhy[2]}\'')
        else:
            data = data.query(f'List == \'{ierarhy[2]}\' and Parent == \'{parent}\'')
    return data['Item Name'].to_list()


def get_items(list_name: str, url: str, cookie: dict, parent: str = ...):
    data = get_list(list_name, url=url, cookie=cookie)
    if parent is ...:
        elements = data.query(f'List == \'{list_name}\'')['Item Name']
    else:
        elements = data.query(f'List == \'{list_name}\' and Parent == \'{parent}\'')['Item Name']
    elements = elements.to_list()
    return elements


def add_item_to_list(list_name: str, item_name: str, url: str, cookie: dict, parent: str= ...):
    if parent is ... :
        data_json = {'Item Name': item_name}
        src_to_dest_column_map = {'Item Name': 'Item Name'}
    else:
        data_json = {'Item Name': item_name, 'Parent': parent}
        src_to_dest_column_map = {'Item Name': 'Item Name', 'Parent':'Parent'}
    param = json.dumps({
        "SRC": {
            "TYPE": 'OM_WEB_SERVICE_PASSIVE',
            "PARAMS": {
            }
        },
        "DEST": {
            "TYPE": 'LIST',
            "PARAMS": {
                "NAME": list_name,
                "TRANSFORM": {
                    "CHARSET": "UTF-8",
                    "SRC_TO_DEST_COLUMN_MAP": src_to_dest_column_map,
                    "DIMENSIONS": {
                    },
                    "CUSTOM_COLUMNS": [],
                    "SRC_COLUMN_PREPARE_DATA_MAP": {}
                },
            }
        },
        "DATA": [data_json]
    })
    response = make_request(url=url, cookie=cookie, request_type='post', data=param)
    
    return


def change_properties(list_name: str, item_name: str, properties: dict, url: str, cookie: dict, parent: str = ...):
    if parent is ... :
        data_json = {'Item Name': item_name}
        src_to_dest_column_map = {'Item Name': 'Item Name'}
    else:
        data_json = {'Item Name': item_name, 'Parent': parent}
        src_to_dest_column_map = {'Item Name': 'Item Name', 'Parent':'Parent'}    
    for i in properties.keys():
        src_to_dest_column_map.update({i:i})
    data_json.update(properties)
    param = json.dumps({
        "SRC": {
            "TYPE": 'OM_WEB_SERVICE_PASSIVE',
            "PARAMS": {
            }
        },
        "DEST": {
            "TYPE": 'LIST',
            "PARAMS": {
                "NAME": list_name,
                "TRANSFORM": {
                    "CHARSET": "UTF-8",
                    "SRC_TO_DEST_COLUMN_MAP": src_to_dest_column_map,
                    "DIMENSIONS": {
                    },
                    "CUSTOM_COLUMNS": [],
                    "SRC_COLUMN_PREPARE_DATA_MAP": {}
                },
            }
        },
        "DATA": [data_json]
    })
    response = make_request(url=url, cookie=cookie, request_type='post', data=param)
    
    return 


def add_item_with_properties(list_name: str, item_name: str, properties: dict, url: str, cookie: dict, parent: str = ...):
    if item_name in get_items(list_name,url,cookie,parent):
        change_properties(list_name, item_name, properties,url,cookie, parent)
    else:
        add_item_to_list(list_name, item_name,url,cookie, parent)
        change_properties(list_name, item_name, properties,url,cookie, parent)


def filter_list_by_property(list_name: str, property_name: str, property_value: str, url: str, cookie: str):
    data = get_list(list_name, url, cookie)
    filtred_data = data.loc[data[property_name] == property_value]
    return filtred_data

