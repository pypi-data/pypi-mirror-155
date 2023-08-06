# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, C0301
from dataskema import util

ES = 'es'
EN = 'en'

DEFAULT = EN

ANONYMOUS_NAME = {
    EN: "It",
    ES: "",
}
PLURAL = {
    EN: "s",
    ES: "es",
}
MORE_MESSAGES = {
    EN: "...and {total} validation error{plural} more",
    ES: "...y {total} error{plural} más",
}


def _get_anonymous() -> str:
    name = ANONYMOUS_NAME.get(DEFAULT)
    if name is None:
        name = ''
    return name


def _get_plural() -> str:
    name = PLURAL.get(DEFAULT)
    if name is None:
        name = PLURAL.get(EN)
    return name


def _get_more_messages() -> str:
    name = MORE_MESSAGES.get(DEFAULT)
    if name is None:
        name = MORE_MESSAGES.get(EN)
    return name


def get_more_messages(total: int) -> str:
    """
    Message for append to general validation message when more messages were found
    :param total: total messages more
    :return: message or '' if no more messages were found
    """
    if total > 0:
        params = {
            'total': str(total),
            'plural': _get_plural() if total > 1 else ''
        }
        return ' ' + get_message(_get_more_messages(), params)
    return ''


def get_message(val_message: str, val_params: dict, anonymize: bool or None = False) -> str:
    ex_message = val_message
    for (key, value) in val_params.items():
        if key == 'name':
            value = "'" + value + "'" if not anonymize else _get_anonymous()
        if value is None:
            value = ''
        ex_message = util.trim(ex_message.replace('{' + key + '}', str(value)))
        ex_message = ex_message[0].upper() + ex_message[1:]
    return ex_message


VAL_ERROR_PARAM_IS_MANDATORY = {
    EN: "{name} is mandatory",
    ES: "{name} es obligatorio",
}
VAL_ERROR_PARAM_HAS_INVALID_TYPE = {
    EN: "{name} has an invalid data type",
    ES: "{name} tiene un tipo de dato no válido",
}
VAL_ERROR_PARAM_HAS_INVALID_FORMAT = {
    EN: "{name} has an invalid format",
    ES: "{name} tiene un formato no válido",
}
VAL_ERROR_PARAM_HAS_INVALID_EMAIL = {
    EN: "{name} has an invalid e-mail format",
    ES: "{name} tiene un formato de URL no válido",
}
VAL_ERROR_PARAM_HAS_INVALID_URL = {
    EN: "{name} has an invalid URL format",
    ES: "{name} tiene un formato de URL no válido",
}
VAL_ERROR_PARAM_IS_TOO_SHORT = {
    EN: "{name} is too short (min. {minsize})",
    ES: "{name} es demasiado corto (mín. {minsize})"
}
VAL_ERROR_PARAM_IS_TOO_LARGE = {
    EN: "{name} is too large (max. {maxsize})",
    ES: "{name} es demasiado largo (máx. {maxsize})",
}
VAL_ERROR_PARAM_IS_TOO_SMALL = {
    EN: "{name} is too small (min. {minvalue})",
    ES: "{name} es demasiado pequeño (mín. {minvalue})",
}
VAL_ERROR_PARAM_IS_TOO_BIG = {
    EN: "{name} is too big (max. {maxvalue})",
    ES: "{name} es demasiado grande (máx. {maxvalue})",
}
VAL_ERROR_LIST_ITEM_HAS_INVALID_ELEMENT = {
    EN: "{name} has an invalid element. {message}",
    ES: "{name} tiene un elemento no válido. {message}",
}
VAL_ERROR_DICT_ITEM_HAS_INVALID_ELEMENT = {
    EN: "{name} has an invalid field. {message}",
    ES: "{name} tiene un campo no válido. {message}",
}
VAL_ERROR_PARAM_HAS_INVALID_VALUE = {
    EN: "{name} has a not valid value",
    ES: "{name} tiene un valor no válido",
}
VAL_ERROR_PARAM_HAS_TOO_MUCH_LINES = {
    EN: "{name} has too much lines (max. {maxlines} lines)",
    ES: "{name} tiene demasiadas lineas (máx. {maxlines} lineas)",
}
VAL_ERROR_PARAM_DATE_FORMAT = {
    EN: "{name} must be a valid date with format {date_format}",
    ES: "{name} debe ser una fecha válida con el formato {date_format}",
}
VAL_ERROR_PARAM_TIME_FORMAT = {
    EN: "{name} must be a valid time with format {time_format}",
    ES: "{name} debe ser una hora válida con el formato {time_format}",
}
VAL_ERROR_PARAM_DATETIME_FORMAT = {
    EN: "{name} must be a valid date and time with format {datetime_format}",
    ES: "{name} debe ser una fecha y hora válida con el formato {datetime_format}",
}
VAL_ERROR_DICT_ITEM_HAS_NOT_DEFINED_DATA_VALIDATION = {
    EN: "{name} has not defined a data validation",
    ES: "{name} no tiene definido una validación del dato",
}
