import logging
import sys
from configparser import ConfigParser
from pathlib import Path
from typing import Dict, Any, OrderedDict

from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    username: str = None
    password: str = None
    host: str = None
    port: int = None
    database: str = "OllamaTgBot"


# class LimitsConfig(BaseModel):
#     . . .
class OllamaConfig(BaseModel):
    url: str = "http://localhost:11434/"
    default_model: str = "dolphin3"

class AppConfig(BaseModel):
    bot_token: str = None
    admin_id: int = None


class InfoConfig(BaseModel):
    version: str = "0.0.1"


class Config(BaseModel):
    APP: AppConfig = AppConfig()
    # LIMITS: LimitsConfig = LimitsConfig()
    DATABASE: DatabaseConfig = DatabaseConfig()
    INFO: InfoConfig = InfoConfig()
    OLLAMA: OllamaConfig = OllamaConfig()


def flatten(d: Dict[str, Any], parent: list[str] = None) -> Dict:
    parent = parent or []
    if any(isinstance(v, dict) for v in d.values()):
        out: Dict[str, Dict] = {}
        for key, val in d.items():
            if isinstance(val, dict) and any(isinstance(v2, dict) for v2 in val.values()):
                out.update(flatten(val, parent + [key]))
            elif isinstance(val, dict):
                section = ".".join(parent + [key])
                out[section] = {
                    k: "" if v is None else str(v)
                    for k, v in val.items()
                }
        return out
    else:
        section = ".".join(parent)
        return {section: {k: "" if v is None else str(v) for k, v in d.items()}}


def get_defaults() -> Dict:
    return flatten(Config().model_dump())


def parse_config_file(config_file: str) -> Dict:
    config_data = {}

    parser = ConfigParser(dict_type=OrderedDict)
    parser.read_dict(get_defaults())
    parser.read(config_file, encoding="utf-8")

    with open(config_file, "w", encoding="utf-8") as f:
        parser.write(f)

    # Проверка на наличие незаполненных значений конфига и завершение работы в случае нахождения
    missing: list[str] = []
    for sect in parser.sections():
        for key, val in parser.items(sect):
            if val == "":
                missing.append(f"{sect}.{key}")
    if missing:
        logging.critical(f"Missing values for: {', '.join(missing)}")
        return sys.exit(1)


    for section in parser.sections():
        main_section = section.split('.')[0]

        if section != main_section:
            secondary_section = section.split('.')[1]
            if main_section in config_data.keys():
                config_data[main_section][secondary_section] = dict(parser.items(section))
            else:
                config_data[main_section] = {}
                config_data[main_section][secondary_section] = dict(parser.items(section))
        else:
            config_data[section] = dict(parser.items(section))

    if len(config_data) == 0:
        raise EnvironmentError("No config file")

    return config_data


def write_default_config(path: str = "config.ini", rewrite: bool = False) -> None:
    parser = ConfigParser()
    parser.read_dict(get_defaults())

    if Path(path).exists() and not rewrite:
        parser.read(path, encoding="utf-8")

    with open(path, "w", encoding="utf-8") as f:
        parser.write(f)
