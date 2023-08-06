from typing import List, Dict, Tuple

from miniut import config as cfg
from miniut import console


__report: Dict[str, List[Tuple[str, str]]] = {}
"""
key: id, group of report
value: a list of tuples of 2 values:
       the first value is a title and the second value is a description
"""


__report_titles: Dict[str, int] = {}
__max_id_len: int = 0


__GENERAL_REPORT_LANG = {cfg.ENG : 'Total of < {id} > with erros {tab} : {n_errors}',
                         cfg.ESP : 'Total de < {id} > con errores {tab} : {n_errors}',
                         }

__BLOCK_LANG_GENERAL = {cfg.ENG : 'General report',
                        cfg.ESP : 'Reporte general'
                        }

__BLOCK_LANG_DETAIL = {cfg.ENG : 'Detail report',
                       cfg.ESP : 'Reporte detallado'
                       }


def resert() -> None:
    """
    Reset the configuration of the report module
    """
    global __report, __max_id_len, __report_titles
    __report: Dict[str, List[Tuple[str, str]]] = {}
    __report_titles: Dict[str, int] = {}
    __max_id_len: int = 0


def init() -> None:
    """
    Initialize the report module
    """
    resert()


def add_id(id: str):
    """
    Add new id, if not exists, to the report module

    Parameters
    ----------
    id : str
        id name of the report
    """
    global __max_id_len
    if id not in __report:
        __report[id] = []
        __max_id_len = max(__max_id_len, len(id))


def add_message_by_id(id: str, title: str, message: str = ''):
    """
    Add a new title with the specified message to the report by the given id,
    if the id does not exist, add the new id before.

    Parameters
    ----------
    id : str
        The id name of the report
    title : str
        The title of the message
    message : str, optional
        The message to be added to the report, by default ''
    """
    add_id(id)
    __report[id].append((title, message))

    global __report_titles
    if id not in __report_titles:
        __report_titles[id] = 0
    __report_titles[id] = max(__report_titles[id], len(title))


def get_val_per_id(id: str) -> list:
    """
    Find and return the value of the report by id.

    Parameters
    ----------
    id : str
        The id name of the report

    Returns
    -------
    list
        List of items by id, titles and their respective messages
    """
    try: items_by_id: list = __report[id]
    except KeyError: items_by_id = None
    return items_by_id


def num_total_values() -> int:
    """
    Count the number of elements (ids) in the report

    Returns
    -------
    int
        Number of the elements (ids) in the report
    """
    n = 0
    for id in __report:
        n += num_elements_by_id(id)
    return n


def num_elements_by_id(id: str) -> int:
    """
    Get the number of elements by the given id

    Parameters
    ----------
    id : str
        The id name of the report

    Returns
    -------
    int
        Number of elements by id
    """
    try:    n = len(get_val_per_id(id=id))
    except: n = 0
    return  n


@console.block(message_block=__BLOCK_LANG_GENERAL)
def print_general_report(color_error: str = console.RED, color_ok: str = console.GREEN) -> None:
    """
    Print the general report by the console, printing in red colour the ids that have
    elements, this is considered as an error, otherwise it prints in green colour the ids

    Parameters
    ----------
    color_error : str, optional
        The colour of id with elements, by default console.RED
    color_ok : str, optional
        The colour of ids ok, by default console.GREEN
    """
    for id in __report:
        n_errors = num_elements_by_id(id)
        color = color_error if n_errors > 0 else color_ok
        tab = '.' * (__max_id_len - len(id))
        console.println(__GENERAL_REPORT_LANG[cfg.lang()].format(id=id, tab=tab, n_errors=n_errors), color=color)


@console.block(message_block=__BLOCK_LANG_DETAIL)
def print_detail_report():
    """
    Print the detailed report, id, title and message
    """
    for id in __report:
        for title, message in __report[id]:
            console.warning(f'{id} : {title} | {message} ')


def general_report_string() -> str:
    """
    Returns the string representation of the general report

    Returns
    -------
    str
        String representation of the general report
    """
    report = ''
    for id in __report:
        n_errors = num_elements_by_id(id)
        tab = '.' * (__max_id_len - len(id))
        report += f'{__GENERAL_REPORT_LANG[cfg.lang()].format(id=id, tab=tab, n_errors=n_errors)}\n'
    return report


def detail_report_string() -> str:
    """
    Return the string representation of the detailed report

    Returns
    -------
    str
        String representation of the detailed report
    """
    report = ''
    for id in __report:
        for title, message in __report[id]:
            report += f'{id} : {title} | {message}\n'
    return report
