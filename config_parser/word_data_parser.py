from .config_parsing_exceptions import (
    ConfigFileNotFoundError,
    CannotDecodeConfigFileAsJsonError,
    NoSuchUnitError,
)
import json
import os


def get_word_data_dir_abspath() -> str:
    return os.path.join(os.path.dirname(__file__), "../word_data")


def parse_word_data_file(
    file_name: str,
    units: str | list[str],
) -> dict[str, list[dict]]:

    word_data_abspath: str = os.path.join(get_word_data_dir_abspath(), file_name)

    if isinstance((units), str):
        units = [units]

    try:
        with open(word_data_abspath, encoding="UTF-8") as f:
            word_data_raw_json = json.load(f)

    except FileNotFoundError:
        raise ConfigFileNotFoundError(file_name)
    except json.JSONDecodeError:
        raise CannotDecodeConfigFileAsJsonError(file_name)

    word_data = {"words": [], "phrases": []}

    for unit in units:

        words_and_phrases = word_data_raw_json.get(unit)
        if words_and_phrases is None:
            raise NoSuchUnitError(unit, file_name)

        word_data["words"].extend(words_and_phrases.get("words", []))
        word_data["phrases"].extend(words_and_phrases.get("phrases", []))

    return word_data


def parse_word_data_files(
    file_name_units_map: dict[str, str | list[str]],
) -> dict[str, list[dict]]:

    word_data = {"words": [], "phrases": []}

    for file_name_and_units in file_name_units_map.items():
        word_data = parse_word_data_file(*file_name_and_units)

        word_data["words"].extend(word_data["words"])
        word_data["phrases"].extend(word_data["phrases"])

    return word_data
