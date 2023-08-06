import logging
import typer

from atlas_engine_client.external_task import ExternalTaskClient

from ..configuration import ConfigAccessor
from . import check_running_process_instance

logger = logging.getLogger('processcube_sdk')

app = typer.Typer()


def setup_logging():
    ConfigAccessor.ensure_from_env()
    config = ConfigAccessor.current()

    logging_level = config.get('logging', 'level')

    log_level = getattr(logging, logging_level.upper(), logging.INFO)

    format_template = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=log_level, format=format_template)

    return logging.getLogger()


def start_external_task():
    ConfigAccessor.ensure_from_env()
    config = ConfigAccessor.current()

    engine_url = config.get('engine', 'url')

    client = ExternalTaskClient(engine_url)

    handler_factories = [
        check_running_process_instance,
    ]

    for factory in handler_factories:
        handler = factory.create_external_task(config)

        logger.info(
            f"Starting external task worker for topic '{handler.get_topic()}'")

        client.subscribe_to_external_task_for_topic(
            handler.get_topic(), handler)

    client.start()


@app.command()
def external_task():
    setup_logging()
    start_external_task()


@app.callback(invoke_without_command=True)
def default():

    setup_logging()
    start_external_task()


if __name__ == '__main__':
    app()
