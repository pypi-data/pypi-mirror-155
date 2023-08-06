import click

import commons.config as config
import utils.logger as logger


def add_default_profile():
    secret_id = click.prompt(logger.style('\n[default] Your default secret_id '),
                             default=config.get_default_env("secret_id"), type=str)
    secret_key = click.prompt(logger.style('\n[default] Your default secret_key  '),
                              default=config.get_default_env("secret_key"), type=str)
    domain = click.prompt(logger.style('\n[default] Your default domain  '),
                          default=config.get_default_env("domain"), type=str)
    region = click.prompt(
        logger.style('\n[default] Your default region, if you don\'t enter it, the default is ap-guangzhou  '),
        default="ap-guangzhou", type=str)
    config.set_env('default', 'secret_id', secret_id)
    config.set_env('default', 'secret_key', secret_key)
    config.set_env('default', 'domain', domain)
    config.set_env('default', 'region', region)


def input_config_vars(profile_name, key_name, is_default_exist):
    if is_default_exist:
        default_value = config.get_env('default', key_name)
        user_input = click.prompt(logger.style('\ndefault value  ' + key_name), default=default_value, type=str)
    else:
        user_input = click.prompt(logger.style('\nYour ' + key_name), type=str)

    config.set_env(profile_name, key_name, user_input)


def add_profile(profile_name):
    config.add_profile(profile_name)
    config.set_env(profile_name, 'profile_name', profile_name)
    input_config_vars(profile_name, 'secret_id', False)
    input_config_vars(profile_name, 'secret_key', False)
    input_config_vars(profile_name, 'domain', False)
    input_config_vars(profile_name, 'region', False)
