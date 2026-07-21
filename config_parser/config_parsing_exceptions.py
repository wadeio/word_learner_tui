import logging

logger = logging.getLogger(__file__)


# The super class of all config parsing exceptions
class ConfigParsingExceptions(Exception): ...


class ConfigMissingEssentialKeyError(ConfigParsingExceptions):
    def __init__(self, key):
        self.key = key
        message = f"Config missing essential key: {key}"
        logger.error(message)
        super().__init__(message)


class ConfigFileNotFoundError(ConfigParsingExceptions):
    def __init__(self, file_name: str):
        self.file_name = file_name
        message = f"Cannot found config file {file_name}"
        logger.error(message)
        super().__init__(message)


class CannotDecodeConfigFileAsJsonError(ConfigParsingExceptions):
    def __init__(self, file_name: str):
        self.file_name = file_name
        message = f"Fail to decode file: '{file_name}' as json"
        logger.error(message)
        super().__init__(message)


class UnsupportedGenerateMethodError(ConfigParsingExceptions):
    def __init__(self, generate_method: str, supported: list | tuple | None = None):
        if supported is None:
            message = f"Unsupported generate method: {generate_method}"

        else:
            message = f"Unsupported generate method: {generate_method}, supported: {' '.join(supported)}"

        logger.error(message)
        super().__init__(message)


class NoSuchUnitError(ConfigParsingExceptions):
    def __init__(self, unit: str, file: str = "UNKNOW"):
        self.unit = unit
        self.file = file
        message = f"No such unit: {unit} in file {file}"
        logger.error(message)
        super().__init__(message)


class DuplicateWordBookNameError(ConfigParsingExceptions):
    def __init__(self, file1_name: str, file2_name: str):
        self.file1_name = file1_name
        self.file2_name = file2_name

        message = f"Word book file {file1_name} has a duplicate word book name with word book file {file2_name}"

        logger.error(message)

        super().__init__(message)
