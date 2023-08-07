import os
import copy
import inspect
import logging
import traceback

from atlas_engine_client.external_task import FunctionalError

logger = logging.getLogger(__name__)


def has_task_param(handle_func):

    def is_handler_a_func(func):
        spec = inspect.getfullargspec(func)
        is_func = inspect.isroutine(func)
        arg_count = len(spec.args)

        result = (arg_count == 2 and is_func)

        logger.info(f"is_handler_a_func: arg_count {arg_count} is_func: {is_func} -> {result}")

        return result

    def is_handler_callable(caller):
        spec = inspect.getfullargspec(caller)
        is_func = inspect.isroutine(caller)
        arg_count = len(spec.args)

        result = (arg_count == 3 and is_func)

        logger.info(f"is_handler_callable: arg_count {arg_count} is_func: {is_func} -> {result}")

        return result

    return is_handler_a_func(handle_func) or is_handler_callable(handle_func)

class BaseHandler(object):

    def __init__(self, topic=None, temp_folder=None):
        self._topic = topic

    def get_topic(self):
        return self._topic

    def handle_task(self, payload, task=None):
        return {}

    def get_temp_folder(self, temp_folder=None):
        if temp_folder is None:
            root_folder = self.get_root_folder()
            temp_folder = os.path.join(root_folder, 'temp')

        if not os.path.isdir(temp_folder) and not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        return temp_folder

    def get_root_folder(self):
        file_folder = os.path.dirname(__file__)
        app_root_folder = os.path.abspath(
            os.path.join(file_folder, '../controlling_platform/data_preparation', '..', '..'))

        return app_root_folder

    def __call__(self, payload, task):
        logger.info(
            f"Running worker for topic {self.get_topic()} with payload {payload}")

        copy_payload = copy.deepcopy(payload)

        try:
            if has_task_param(self.handle_task):
                logger.info("Calling handler with task")
                result = self.handle_task(payload, task)
            else:
                logger.info("Calling handler without task")
                result = self.handle_task(payload)

            logger.info(f"Handle task {self.get_topic()} with result '{result}'")

            copy_payload.update(result)
            logger.info(
                f"Finished worker for topic {self.get_topic()} with result {copy_payload}")

        except Exception as e:
            formatted_lines = traceback.format_exc().splitlines()
            raise FunctionalError('ProcessingFailed', str(formatted_lines))
            logger.error(
                f"Finished worker for topic {self.get_topic()} with error 'ProcessingFailed")

        return copy_payload


