import json
import logging
import os

logger = logging.getLogger(__file__)

class Config:

    def __init__(self, config: dict):
        self._config = config

    def get(self, *parts: str, default=None):
        config_value = default

        current_config = self._config

        assert current_config is not None, f"current_config is empty '{current_config}'"

        for part in parts:
            if not type(current_config) == dict:
                assert default is not None, f"{'->'.join(parts)} not in {self._config}."

                config_value = default
                break

            assert (current_config is not None and part in current_config.keys()) or default is not None, f"{part} missing is not given in {current_config}; {'->'.join(parts)} not in {self._config}"

            current_config = current_config.get(part, config_value)

            config_value = current_config

        return config_value

    @staticmethod
    def from_env(env_name='CONFIG_FILE'):
        filename = os.environ.get(env_name)

        assert filename is not None, f"{env_name} is not given."

        return Config.from_file(filename)

    @staticmethod
    def from_file(filename: str):
        assert os.path.isfile(filename), f"{filename} did'nt exist or is not a file"

        with open(filename) as f:
            data = json.load(f)

        config = Config(data)

        return config

    @staticmethod
    def from_json_str(json_string: str):

        data = json.loads(json_string)

        config = Config(data)

        return config

if __name__ == '__main__':
    d = {
        'hello': 'world',
        'sample_service': {
                'config_key': 'config_value'
            }
        }
    c = Config(d)

    print(c.get('hello'))
    print(c.get('helo', default='default'))
    print(c.get('sample_service', 'config_key', default='default_value'))
