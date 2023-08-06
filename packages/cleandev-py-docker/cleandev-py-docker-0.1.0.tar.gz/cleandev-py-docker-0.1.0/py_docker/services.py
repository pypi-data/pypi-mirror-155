import json
import docker
from py_docker.parser import service_to_basic_info
from py_docker.task import SummaryTaskInfo

api = docker.from_env().api


class SummaryServiceInfo:

    @staticmethod
    def get_services_info():
        '''

            Usa la plantilla `service_to_basic_info` para extraer los datos `{ 'id_service': '', 'replicas': 0, }` y
            porteriormente añade `runnig` que son los contenedores que actualmente estan corriendo dicho servicio
            y evalua si el estado del servicio esta `OK`, `WARNING` o`KO`

                - OK: Un servicio se considera "OK" cuando rc == dr donde rc=running-container y dr=desired-runnig
                      o dicho de otra manera cuando existen tantos contenedores como replicas deseadas
                - WARNING: Un servicio se considera "WARNING" cuando rc > 1 && rc < dr donde rc=running-container y
                           dr=desired-runnig o dicho de otra manera cuando los contenedores que estan corriendo al menos
                           existe uno corriendo pero son menores a los contenedores que deseamos que esten corriendo
                - OK: Un servicio se considera "KO" cuando rc == 0 donde rc=running-container o dicho de otro modo
                      cuando no hay ningun contenedor corriendo, se sobreentiende que en el momento que un servicio
                      es levantado al menos debe existir un contenedor que ejecute dicho servicio ya que si no, no
                      existiria dicho servicio
            El diccionario resultante de la operacion es:
            {                                               |   {
                "id_service": "1z1nlvwth223o3mhk7r9k2t0q",  |       "id_service": "1z1nlvwth223o3mhk7r9k2t0q",
                "replicas": 5,                              |       "replicas": 10,
                "running": 5,                               |       "running": 5,
                "status": "OK"                              |       "status": "WARNING",
            }                                               |   }
        '''
        number_nodes: int = len(api.nodes())
        items: list = []
        for service in api.services():
            temp_data: dict = service_to_basic_info(service, number_nodes)
            number_container_running: int = SummaryTaskInfo.get_container_runnig_by_service(temp_data['id_service'])
            temp_data['running'] = number_container_running

            if number_container_running == int(temp_data['replicas']):
                temp_data['status'] = 'OK'

            if number_container_running != int(temp_data['replicas']) and number_container_running > 0:
                temp_data['status'] = 'WARNING'

            if number_container_running == 0:
                temp_data['status'] = 'KO'

            items.append(temp_data)

        generic_status: str = 'OK'
        for item in items:
            if item['status'] == 'KO':
                generic_status = 'KO'
                break
            if item['status'] == 'WARNING':
                generic_status = 'WARNING'

        return {'services': items, 'status': generic_status}
