import logging

from atlas_engine_client.core.api import Client, ProcessInstanceQueryRequest

from ...configuration import Config
from ..base_handler import BaseHandler

DEFAULT_ENGINE_URL = 'http://localhost:56100'

logger = logging.getLogger(__name__)

class CheckRunningProcessInstanceHandler(BaseHandler):
    def __init__(self, config: Config):
        super().__init__('check_running_process_instance')
        self._engine_url = config.get('engine', 'url', default=DEFAULT_ENGINE_URL)

    def handle_task(self, _, task):
        process_model_id = task.get('processModelId', 'missing id')
        process_instance_id = task.get('processInstanceId', 'missing id')

        logger.debug(">>>>>>>>>>>>>>>>>>")
        logger.debug(process_model_id)
        logger.debug(process_instance_id)
        logger.debug("<<<<<<<<<<<<<<<<<<")

        running = False
        other_instance_count = 0

        try:
            query = ProcessInstanceQueryRequest(process_model_id=process_model_id, state="running")

            api_client = Client(self._engine_url)
            result = api_client.process_instanceq_query(query)

            filtered_result = filter(lambda entry: entry.process_instance_id != process_instance_id, result)

            other_instance_count = len(list(filtered_result))

            running = (other_instance_count != 0)
        except Exception as e:
            logger.error(f"Cannot request instances {e}")
            running = True
            
        other_instance = {'other_instance': {
            'running': running,
            'not_running': not running,
            'count': other_instance_count,
        }}

        logger.info(f"check '{process_model_id}' for '{process_instance_id}' results in '{other_instance}'.")

        return other_instance

def create_external_task(config: Config) -> BaseHandler:
    handler = CheckRunningProcessInstanceHandler(config)

    return handler

