import glob
import json
import logging
import os

from .config_parsing_exceptions import (
    CannotDecodeConfigFileAsJsonError,
    ConfigFileNotFoundError,
    ConfigMissingEssentialKeyError,
    ConfigParsingExceptions,
    DuplicateWordBookNameError,
    UnsupportedGenerateMethodError,
)
from .word_data_parser import parse_word_data_file, parse_word_data_files

logger = logging.getLogger(__name__)


def parse_manual_entry(config: dict) -> tuple[str, dict]:
    name = config.get("name", "Unnamed")

    file_name_units_map = config.get("file_name_units_map")

    if file_name_units_map is None:
        raise ConfigMissingEssentialKeyError("file_name_units_map")

    word_data = parse_word_data_files(file_name_units_map)

    return name, word_data


def parse_manual_group(config: dict) -> tuple[str, dict[str, dict]]:
    group_name = config.get("name", "Unnamed")
    entry_name_word_data_map = {}

    entries = config.get("entries")

    if entries is None:
        raise ConfigMissingEssentialKeyError("entries")

    if not isinstance(entries, list):
        entries = [entries]

    for entry in entries:
        entry_name_and_word_data = parse_manual_entry(entry)

        entry_name_word_data_map[entry_name_and_word_data[0]] = (
            entry_name_and_word_data[1]
        )

    return group_name, entry_name_word_data_map


def parse_auto_group(config: dict) -> tuple[str, dict[str, dict]]:
    group_name = config.get("name", "Unnamed")
    unit_name_word_data_map = {}

    file_name_units_map = config.get("file_name_units_map")

    if file_name_units_map is None:
        raise ConfigMissingEssentialKeyError("file_name_units_map")

    for file_name, units in file_name_units_map.items():
        # make sure unit is a list
        if not isinstance(units, list):
            units = [units]

        for unit in units:
            if isinstance(unit, str):
                unis = [unit]

            unit_name_word_data_map[" and ".join(unis)] = parse_word_data_file(
                file_name, unit
            )

    return group_name, unit_name_word_data_map


def parse_word_book_content(content: dict | list) -> dict:
    if isinstance(content, dict):
        content = [content]

    content_map = {}

    for group_or_entry in content:
        generate_method = group_or_entry.get("generate_method")

        # match ervery generate_method
        if generate_method is None:
            name, data = parse_manual_entry(group_or_entry)

        elif generate_method == "manual":
            name, data = parse_manual_group(group_or_entry)

        elif generate_method == "auto":
            name, data = parse_auto_group(group_or_entry)

        else:
            raise UnsupportedGenerateMethodError(generate_method)

        content_map[name] = data

    return content_map


def parse_word_book(word_book: dict) -> tuple[str, dict]:

    name = word_book.get("name", "Unnamed")
    content = word_book.get("content")

    if content is None:
        raise ConfigMissingEssentialKeyError(content)

    return name, parse_word_book_content(content)


def get_word_book_config_dir_abspath() -> str:
    return os.path.join(os.path.dirname(__file__), "../word_book_configs")


def parse_word_book_file(file_name: str) -> tuple[str, dict]:
    file_abspath = os.path.join(get_word_book_config_dir_abspath(), file_name)

    try:
        with open(file_abspath) as f:
            word_book = json.load(f)

    except FileNotFoundError:
        raise ConfigFileNotFoundError(file_name)
    except json.JSONDecodeError:
        raise CannotDecodeConfigFileAsJsonError(file_name)

    return parse_word_book(word_book)


def parse_all_word_books() -> dict:

    word_book_config_dir_abspath = get_word_book_config_dir_abspath()
    word_books = {}

    word_book_name_file_name_map = {}

    for file_abspath in glob.glob(os.path.join(word_book_config_dir_abspath, "*.json")):
        file_name = os.path.basename(file_abspath)

        logger.info(f"----------Start parsing word_book file {file_name}----------")

        try:
            word_book_name, word_book_content = parse_word_book_file(file_name)

            if word_book_name in word_books:
                raise DuplicateWordBookNameError(
                    file_name, word_book_name_file_name_map[word_book_name]
                )

            word_book_name_file_name_map[word_book_name] = file_name

            word_books[word_book_name] = word_book_content
            logger.info(f"word_book file {file_name} have been successfully parsed")

        # handle exceptions, if the exception is a designed error, just log it, else
        # show the detail of the exception
        except Exception as e:
            need_show_exception = not issubclass(type(e), ConfigParsingExceptions)
            logger.error(
                f"Error when parsing word_book file {file_name}",
                exc_info=need_show_exception,
            )

    return word_books


# for test
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    data = parse_all_word_books()
    fd = json.dumps(data, ensure_ascii=False, indent=4)
    print(fd)
