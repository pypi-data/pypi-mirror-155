"""Settings config"""
from os.path import dirname, join, exists

from dynaconf import Dynaconf, Validator

module_path = dirname(__file__)

settings_file = join(module_path, "settings.toml")

if exists(settings_file):
    settings = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_file=settings_file
        )

    settings.validators.register(
        Validator(
            "logging_auto_create_dir",
            "logging_log_to_file",
            "color",
            is_type_of=bool,
            ),
        Validator(
            "logging_path",
            "logging_ext",
            "spacer",
            "spacer_color",
            is_type_of=str,
            ),
        Validator(
            "specific_loggers",
            is_type_of=dict,
            ),
        )
    settings.validators.validate()

else:
    settings = ""
