def node_to_node_summary(data: dict):
    '''

        Recibe como parametro un item de la lista `api.nodes()` que representa toda
        la información referente a un nodo y devuelve un objeto resumido del mismo
        Objeto a retornar
        {
            'id': '',
            'hostname': '',
            'engine_version': '',
            'status': '',
            'manager_status': '',
            'manager_addr': ''
        }
    '''
    result: dict = {
        'id': data['ID'],
        'hostname': data['Description']['Hostname'],
        'engine_version': data['Description']['Engine']['EngineVersion'],
        'status': data['Status']['State'],
    }
    if data.get('ManagerStatus'):
        result['manager_status'] = data['ManagerStatus']['Reachability']
        result['manager_addr'] = data['ManagerStatus']['Addr']
    return result


def service_to_service_summary(data: dict):
    '''

        {
            'id': '',
            'name': '',
            'hash_image': '',
            'mode': '',
            'replicas': '',
        }
    '''

    result: dict = {
        'id': data['ID'],
        'name': data['Spec']['Name'],
        'hash_image': data['Spec']['TaskTemplate']['ContainerSpec']['Image'],
        'mode': list(dict(data['Spec']['Mode']).keys())[0],
        'replicas': data['Spec']['Mode'][list(dict(data['Spec']['Mode']).keys())[0]],
    }
    return result


def service_to_basic_info(data: dict, number_nodes: int):
    '''
        Recoge el id del servicio y el numero de contenedores que deben estar corriendo este servicio.
        Existen dos modos, modo replicas que lleva asociado un numero definido de contenedores que están corriendo
        o el modo global que obliga a que corra uno por nodo.
        {
            'id_service': '',
            'replicas': 0,
        }
    '''

    result: dict = {
        'id_service': data['ID'],
    }
    if 'Global' in data['Spec']['Mode']:
        result['replicas'] = number_nodes
        return result
    result['replicas'] = data['Spec']['Mode']['Replicated']['Replicas']
    return result




