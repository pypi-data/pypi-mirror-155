import os
import yaml
from collections import defaultdict


CONFIG_PATH = "config"


def load_configuration(environment):
    configuration_filepath = os.path.join(CONFIG_PATH, '{}.yml'.format(environment.lower()))

    assert os.path.exists(configuration_filepath), "Configuration file {} not found!".format(configuration_filepath)

    with open(configuration_filepath, 'r') as file:
        configuration = yaml.safe_load(file)

    return defaultdict(dict, configuration)
