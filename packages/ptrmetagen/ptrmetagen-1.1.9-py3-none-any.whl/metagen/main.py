from metagen.config.config import load_yaml, BASE_CONFIG_FILE, Config
from metagen.register import register_factory


CONFIG = Config(**load_yaml(BASE_CONFIG_FILE))
register = register_factory.get(CONFIG.register_setting.registerName)()
