class ConfigMissingEssentialKeyError(Exception):
    def __init__(self, key):
        self.key = key
        super().__init__(f"Config missing essential key: {key}")


class ConfigFileNotFoundError(Exception):
    def __init__(self, file_name: str):
        self.file_name = file_name
        super().__init__(f"Cannot found config file {file_name}")


class CannotDecodeConfigFileAsJsonError(Exception):
    def __init__(self, file_name: str):
        self.file_name = file_name

        super().__init__(f"Fail to decode file: '{file_name}' as json")


class UnsupportedGenerateMethodError(Exception):
    def __init__(self, generate_method: str, supported: list | tuple | None = None):
        if supported is None:
            message = f"Unsupported generate method: {generate_method}"

        else:
            message = f"Unsupported generate method: {generate_method}, supported: {' '.join(supported)}"

        super().__init__(message)


class NoSuchUnitError(Exception):
    def __init__(self, unit: str, file: str = "UNKNOW"):
        self.unit = unit
        self.file = file
        super().__init__(f"No such unit: {unit} in file {file}")


if __name__ == "__main__":
    ...
