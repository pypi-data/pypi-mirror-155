import json
import docker
from py_docker.parser import service_to_basic_info

api = docker.from_env().api


class SummaryTaskInfo:

    @staticmethod
    def get_container_runnig_by_service(id_service: str):
        filter: dict = {'desired-state': 'running', 'service': id_service}
        count_service_running: int = 0
        for task in api.tasks(filters=filter):
            if task['Status']['State'] == 'running':
                count_service_running += 1
        return count_service_running
