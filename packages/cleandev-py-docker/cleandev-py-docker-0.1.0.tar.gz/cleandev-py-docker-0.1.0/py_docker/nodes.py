import docker
from py_docker.parser import node_to_node_summary

api = docker.from_env().api


class SummaryNodeInfo:
    '''
        Metodos relacionado con la obtencion de datos sobre los nodos
    '''

    @staticmethod
    def get_nodes_info() -> dict:
        items: dict = {}
        list_nodes: list = []
        for node in api.nodes():
            list_nodes.append(node_to_node_summary(node))
        items['nodes'] = list_nodes
        return items


class SummaryClusterInfo:
    '''
        Metodos relacionado con datos sobre el cluster dado que existen diferentes configuraciones de nodos
        para maquinas de pre y pro se seguiran estas reglas para la evaluacion de dicho nodo.

        Estado del cluster:
            * OK: El cluster tiene al menos 3 Managers y 2 Workers y TODOS sus nodos estan operativos
            * WARNING: El cluster esta comprometido ya que no hay redundancia de tipos de nodos, es decir
                       que en el caso de que un nodo cae el cluster se ve comprometido aunque ello implique
                       que todos sus nodos esten activos.
            * ERROR: El cluster está comprometido, esto es debido a que al cluster le falta uno de los dos roles
                     del tipo de nodo, (Worker|Manager) y por lo tanto no puede desempeñar su funcion correctamente.
    '''

    @staticmethod
    def get_status_cluster() -> str:
        options_status: dict = {
            0: 'OK',
            1: 'WARNING',
            2: 'KO'
        }

        info_nodes: dict = SummaryNodeInfo.get_nodes_info()
        status_data: dict = {
            'total_nodes': 0,
            'total_readys': 0,
            'workers': {'total': 0, 'ready': 0},
            'managers': {'total': 0, 'ready': 0},
            'status': ''
        }

        for node in info_nodes['nodes']:
            status_data['total_nodes'] += 1
            if dict(node).get('manager_status'):
                status_data['managers']['total'] += 1
                if dict(node).get('status') == 'ready':
                    status_data['managers']['ready'] += 1
                    status_data['total_readys'] += 1
            else:
                status_data['workers']['total'] += 1
                if dict(node).get('status') == 'ready':
                    status_data['workers']['ready'] += 1
                    status_data['total_readys'] += 1

        # Si hay mas de 3 managers y mas de 2 workers y los nodos estan todos activos es OK
        if status_data['workers']['total'] >= 2 and status_data['managers']['total'] >= 3:
            if status_data['total_nodes'] == status_data['total_readys']:
                status_data['status'] = options_status[0]
                return {'status_cluster': status_data}

        if status_data['workers']['total'] == 1 or status_data['managers']['ready'] <= 3:
            if status_data['workers']['ready'] > 0 and status_data['managers']['ready'] > 0:
                status_data['status'] = options_status[1]
                return {'status_cluster': status_data}

        if status_data['workers']['ready'] == 0 or status_data['managers']['ready'] == 0:
            status_data['status'] = options_status[2]
            return {'status_cluster': status_data}
