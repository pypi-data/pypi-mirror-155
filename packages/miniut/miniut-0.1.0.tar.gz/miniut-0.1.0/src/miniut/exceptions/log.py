class LoggingGeneralException(Exception): ...

class RestoreLog(LoggingGeneralException):
    def __init__(self, message: str = None, error: str = ''):
        msg = ''
        if message is None:
            msg = f'Impossible to restore log'
        else:
            msg = f'{message} | {error}'

        super().__init__(msg)

