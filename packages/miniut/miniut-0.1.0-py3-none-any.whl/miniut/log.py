import os
import logging
import functools
from datetime import datetime as dt

from miniut.exceptions import RestoreLog
from miniut import config as cfg


FOLDER_LOGS_DEFAULT: str = 'Logs'

__folder_logs: str    = FOLDER_LOGS_DEFAULT
__log: logging.Logger = None
__log_name: str = 'logging.log'
__log_ok: bool  = True
__log_aux: str  = ''

__lvl: str = ''
__STANDARD_LVL: str = ' '
__LVL_INDENT: int = 2


_START_LANGS = {cfg.ENG : 'START',
                cfg.ESP : 'INICIA',
                }

_END_LANGS = {cfg.ENG : 'END',
              cfg.ESP : 'TERMINA',
              }

_RESTORED_LOG_LANGS = {cfg.ENG : 'RESTORED',
                       cfg.ESP : 'RECONSTRUIDO',
                       }

_RESTORE_EXCEPT_LANGS = {cfg.ENG : 'Impossible to restore log',
                         cfg.ESP : 'No ha sido posible reconstruir el log',
                         }

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                         decorators                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def block(message_block: str or dict):
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            message = message_block
            if isinstance(message_block, dict):
                message = message_block[cfg.lang()]
            start_block(message)
            value = func(*args, **kwargs)
            end_block(message)
            return value
        return wrapped
    return decorator


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                          functions                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def init(log_name: str = 'logging',
         folder_log: str = FOLDER_LOGS_DEFAULT,
         time: bool = True
         ) -> None:
    """
    Initialize the logging module

    Parameters
    ----------
    log_name : str
        Name of logging file
    folder_log : str, optional
        Folder where the logging file should be stored, by default 'Logs'
    time : bool, optional
        True in case the logging file name has the time with format '%Y%m%d-%H%M%S'
        False in case the time in the name is not necessary, by default True
    """
    global __log_name, __folder_logs, __log, __lvl

    __lvl = ''

    log_time: str = dt.now().strftime('%Y%m%d-%H%M%S') if time else ''
    __log_name = f'{log_name} - {log_time}.log'
    __folder_logs = folder_log

    if not os.path.exists(__folder_logs):
        os.makedirs(__folder_logs)

    format = logging.Formatter('%(asctime)-8s - %(levelname)-8s - %(message)s')
    heandler = logging.FileHandler(f'{__folder_logs}/{__log_name}', encoding='UTF-8')
    heandler.setFormatter(format)
    __log = logging.getLogger(__log_name)
    __log.setLevel(logging.DEBUG)
    __log.addHandler(heandler)


def get_folder_log() -> str:
    return __folder_logs


def get_log_name() -> str:
    return __log_name


def _add_lvl() -> None:
    """
    Add one level (indentation)
    """
    global __lvl
    __lvl += (__STANDARD_LVL * __LVL_INDENT)


def _sub_lvl() -> None:
    """
    Substract one level (indentation)
    """
    global __lvl
    __lvl = __lvl[:-__LVL_INDENT]


def _bad_log() -> None:
    """
    Indicate the log has an error and should be restored
    """
    global __log_ok
    __log_ok = False


def start_block(message: str) -> None:
    """
    Start a block of messages

    Parameters
    ----------
    message : str
        The title of the block
    """
    info(f'# {_START_LANGS[cfg.lang()]} {message.upper()} #')
    _add_lvl()


def end_block(message: str) -> None:
    """
    End a block of messages

    Parameters
    ----------
    message : str
        The title of the block
    """
    _sub_lvl()
    info(f'# {_END_LANGS[cfg.lang()]} {message.upper()} #')


def _message_log_aux(type_message: str, msg: str) -> None:
    """
    Put message to display in the log in case will be necessary to restore

    Parameters
    ----------
    type_message : str
        Type of message like 'INFO', 'WARNING', 'ERROR', etc.
    msg : str
        The message to display in the log
    """
    global __log_aux
    log_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
    __log_aux += f'{log_time} - {type_message:<10} - {msg}\n'


def info(message: str) -> None:
    """
    Information message into the log

    Parameters
    ----------
    message : str
        The message to display in the log
    """
    msg = f'{__lvl}{message}'
    try:
        __log.info(msg)
    except:
        _bad_log()
    finally:
        _message_log_aux(type_message='INFO', msg=msg)


def warning(message: str) -> None:
    """
    Warning message into the log

    Parameters
    ----------
    message : str
        The message to display in the log
    """
    msg = f'{__lvl}{message}'
    try:
        __log.warning(msg)
    except:
        _bad_log()
    finally:
        _message_log_aux(type_message='WARNING', msg=msg)


def critical(message: str) -> None:
    """
    Critial message to display in the log

    Parameters
    ----------
    message : str
        The message to display in the log
    """
    msg = f'{__lvl}{message}'
    try:
        __log.critical(msg)
    except:
        _bad_log()
    finally:
        _message_log_aux(type_message='CRITICAL', msg=msg)


def error(message: str) -> None:
    """
    Error message to display in the log

    Parameters
    ----------
    message : str
        The message to display in the log
    """
    msg = f'{__lvl}>>> {message} <<<'
    try:
        __log.error(msg)
    except:
       _bad_log()
    finally:
        _message_log_aux(type_message='ERROR', msg=msg)


def _restore_log() -> None:
    """
    Try to restore the log file at the current location.

    Raises
    ------
    RestoreLog
        In case the log file cannot be restored
    """
    log_file_name = f'{__log_name[:-4]} - {_RESTORED_LOG_LANGS[cfg.lang()]}.log'

    try:
        with open(f'{__folder_logs}/{log_file_name}', 'w', encoding='UTF-8') as f:
            f.write(__log_aux)
    except Exception as e:
        raise RestoreLog(message=_RESTORE_EXCEPT_LANGS[cfg.lang()],
                            error=str(e)
                            )


def close() -> None:
    """
    If the log file had any problem to write then try to restore it.
    """
    if not __log_ok:
        _restore_log()
