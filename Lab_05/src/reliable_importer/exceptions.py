class ImporterError(Exception):
    pass


class InvalidRecordError(ImporterError):
    pass


class ConfigurationError(ImporterError):
    pass
