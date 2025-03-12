import os
from pyaml_env import parse_config
from dotenv import load_dotenv

ENV = os.getenv("APP_ENV", "local")


class AppConfig:
    __instance = None

    # """Implement Singleton Pattern
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(AppConfig, cls).__new__(cls)
            cls.__instance.__init__()

        return cls.__instance

    def __init__(self):
        self.app_env = "local"
        self.config = {}
        self.load_app_configuration()

    def load_app_configuration(self):
        self.load_environment_variables()
        self.load_config_yaml_file()

    def load_environment_variables(self):
        load_dotenv(".env")
        self.app_env = os.getenv("APP_ENV", "local").lower()

    def load_config_yaml_file(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_file_path = os.path.join(base_dir, f"settings_{self.app_env}.yml")

            if not os.path.exists(config_file_path):
                raise FileNotFoundError(f"Configuration file not found: {config_file_path}")

            self.config = parse_config(path=config_file_path)

        except Exception as e:
            raise RuntimeError(f"Failed to load configuration: {str(e)}")
