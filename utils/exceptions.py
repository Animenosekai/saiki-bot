from utils.log import LogLevels, log


class SaikiException(Exception):
    SAFE_MESSAGE = "{mention} ❌ An error occured while processing your request"

    def __init__(self, message: str, *args: object) -> None:
        log(message, level=LogLevels.ERROR)
        super().__init__(*args)


class PageNotNumber(SaikiException):
    SAFE_MESSAGE = "{mention} ❌ Une des pages fournie ne semble pas être un nombre entier"

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)


class ExerciceNotNumber(SaikiException):
    SAFE_MESSAGE = "{mention} ❌ Un des exercices fournie ne semble pas être un nombre entier"

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)


class RequestError(SaikiException):
    SAFE_MESSAGE = "{mention} ❌ An error occured while making a request to process your request"

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)
