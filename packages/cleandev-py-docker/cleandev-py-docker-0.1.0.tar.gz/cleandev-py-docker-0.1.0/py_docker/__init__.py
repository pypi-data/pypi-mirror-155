from .nodes import SummaryNodeInfo
from .nodes import SummaryClusterInfo
from .services import SummaryServiceInfo


class SummaryInfo:
    '''
        Agrupacion de metodos relacionados para obtener informacion del estado del sistema
        en lineas generales
    '''

    @staticmethod
    def generic_status():
        data: dict = SummaryClusterInfo.get_status_cluster()
        data = data | SummaryNodeInfo.get_nodes_info()
        data = data | SummaryServiceInfo.get_services_info()
        return data

    @staticmethod
    def nodes_info():
        data: dict = SummaryNodeInfo.get_nodes_info()
        return data

    @staticmethod
    def cluster_status():
        data: dict = SummaryClusterInfo.get_status_cluster()
        return data

    @staticmethod
    def services_status():
        data: dict = SummaryServiceInfo.get_services_info()
        return data

