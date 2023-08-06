# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, C0301
from dataskema import lang


class DataTypes:

    @staticmethod
    def positive(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'type': 'int',
            'min-value': 1,
            'message': {
                lang.EN: "{name} must be an integer positive number",
                lang.ES: "{name} debe ser un número entero positivo",
            }
        }, ptyp2)

    @staticmethod
    def negative(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'type': 'int',
            'max-value': -1,
            'message': {
                lang.EN: "{name} must be an integer negative number",
                lang.ES: "{name} debe ser un número entero nagativo",
            }
        }, ptyp2)

    @staticmethod
    def zero_positive(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'type': 'int',
            'min-value': 0,
            'message': {
                lang.EN: "{name} must be an integer number or zero",
                lang.ES: "{name} debe ser un número entero positivo o cero",
            }
        }, ptyp2)

    @staticmethod
    def zero_negative(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'type': 'int',
            'max-value': 0,
            'message': {
                lang.EN: "{name} must be an integer negative number or zero",
                lang.ES: "{name} debe ser un número entero negativo o cero",
            }
        }, ptyp2)

    @staticmethod
    def decimal(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'type': 'float',
            'message': {
                lang.EN: "{name} must be a valid decimal number",
                lang.ES: "{name} debe ser un número decimal válido",
            }
        }, ptyp2)

    @staticmethod
    def hexadecimal(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'regexp': '^[A-Fa-f0-9]+$',
            'message': {
                lang.EN: "{name} must be a valid hexadecimal number",
                lang.ES: "{name} debe ser un número hexadecimal válido",
            }
        }, ptyp2)

    @staticmethod
    def base64(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'regexp': '^[A-Za-z0-9+/]+\\={0,2}$',
            'message': {
                lang.EN: "{name} must be a valid base64 string",
                lang.ES: "{name} debe ser una cadena en base64 válida",
            }
        }, ptyp2)

    @staticmethod
    def numeric(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'regexp': '^[0-9]+$',
            'message': {
                lang.EN: "{name} must be a numeric string",
                lang.ES: "{name} debe ser una cadena numérica",
            }
        }, ptyp2)

    @staticmethod
    def alphanumeric(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'regexp': '^[A-Za-z0-9]+$',
            'message': {
                lang.EN: "{name} must be a alphanumeric string",
                lang.ES: "{name} debe ser una cadena alfanumérica",
            }
        }, ptyp2)

    @staticmethod
    def short_id(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'max-size': 20,
        }, ptyp2)

    @staticmethod
    def long_id(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'max-size': 40,
        }, ptyp2)

    @staticmethod
    def short_name(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'max-size': 50,
        }, ptyp2)

    @staticmethod
    def name(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'max-size': 100,
        }, ptyp2)

    @staticmethod
    def title(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'max-size': 200,
        }, ptyp2)

    @staticmethod
    def summary(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'max-size': 2000,
        }, ptyp2)

    @staticmethod
    def text(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'max-size': 500000,
            'max-lines': 10000,
        }, ptyp2)

    @staticmethod
    def version(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'regexp': '^[a-zA-Z0-9\\.\\-\\+]+$',
            'message': {
                lang.EN: "{name} must have a valid version format",
                lang.ES: "{name} debe tener un formato de versión válido",
            }
        }, ptyp2)

    @staticmethod
    def search(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'max-size': 50,
        }, ptyp2)

    @staticmethod
    def email(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'regexp': '^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$',
            'max-size': 100,
            'message': {
                lang.EN: "{name} must have a valid e-mail format",
                lang.ES: "{name} debe tener un formato de e-mail válido",
            }
        }, ptyp2)

    @staticmethod
    def url(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'regexp': '^((((https?|ftps?|gopher|telnet|nntp)://)|(mailto:|news:))(%[0-9A-Fa-f]{2}|[-()_.!~*\';/?:@&'
                      '=+$,A-Za-z0-9])+)([).!\';/?:,][[:blank:|:blank:]])?$',
            'max-size': 500,
            'message': {
                lang.EN: "{name} must have a valid URL format",
                lang.ES: "{name} debe tener un formato de URL válida",
            }
        }, ptyp2)

    @staticmethod
    def password(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'regexp': '^[a-zA-Z0-9_+&*\\$\\-\\(\\)]+$',
            'max-size': 50,
            'min-size': 8,
            'message': {
                lang.EN: "{name} must have a valid password (only alphanumeric chars and _, +, &, *, -, (, ) or $ symbols)",
                lang.ES: "{name} debe tener un formato de password válida (sólo caracters alfanuméricos y los símbolos _, +, &, *, -, (, ) o $",
            }
        }, ptyp2)

    @staticmethod
    def type(ptype: dict, ptyp2: dict or None = None) -> dict:
        ptype = dict(ptype)
        if ptyp2 is not None:
            ptype.update(ptyp2)
        return ptype

    @staticmethod
    def bool(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'type': 'bool',
            'message': {
                lang.EN: "{name} must be a boolean",
                lang.ES: "{name} debe ser un booleano",
            }
        }, ptyp2)

    @staticmethod
    def int(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'type': 'int',
            'message': {
                lang.EN: "{name} must be an integer number",
                lang.ES: "{name} debe ser un número entero",
            }
        }, ptyp2)

    @staticmethod
    def float(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'type': 'float',
            'message': {
                lang.EN: "{name} must be an decimal number",
                lang.ES: "{name} debe ser un número decimal",
            }
        }, ptyp2)

    @staticmethod
    def str(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'type': 'str',
            'message': {
                lang.EN: "{name} must be a valid string",
                lang.ES: "{name} debe ser una cadena de texto válida",
            }
        }, ptyp2)

    @staticmethod
    def white_list(white_list: list, ptyp2: dict or None = None) -> dict:
        return DataTypes.type({'white-list': white_list}, ptyp2)

    @staticmethod
    def list(schema: dict, ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'type': 'list',
            'schema': schema,
            'iduplicated': True,
            'iempty': True,
            'message': {
                lang.EN: "{name} must be a list",
                lang.ES: "{name} debe ser una lista",
            }
        }, ptyp2)

    @staticmethod
    def str_list(schema: dict, ptyp2: dict or None = None) -> dict:
        return DataTypes.type(DataTypes.list(schema, {
            'cast': {
                'type': 'str',
                'join': ','
            },
            'message': {
                lang.EN: "{name} must be a string comma-separated list",
                lang.ES: "{name} debe ser una lista de elementos separados por comas",
            }
        }), ptyp2)

    @staticmethod
    def dict(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'type': 'dict',
            'message': {
                lang.EN: "{name} must be a collection",
                lang.ES: "{name} debe ser una colección",
            }
        }, ptyp2)

    @staticmethod
    def date(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'type': 'date',
            'format': '%Y-%m-%d',
            'message': {
                lang.EN: "{name} must be a valid date with format YYYY-MM-DD",
                lang.ES: "{name} debe ser una fecha válida con el formato YYYY-MM-DD",
            }
        }, ptyp2)

    @staticmethod
    def time(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'type': 'time',
            'format': '%H:%M:%S',
            'message': {
                lang.EN: "{name} must be a valid time with format HH:MM:SS",
                lang.ES: "{name} debe ser una hora válida con el formato HH:MM:SS",
            }
        }, ptyp2)

    @staticmethod
    def datetime(ptyp2: dict or None = None) -> dict:
        return DataTypes.type({
            'type': 'datetime',
            'format': '%Y-%m-%d %H:%M:%S',
            'message': {
                lang.EN: "{name} must be a valid date and time with format YYYY-MM-DD HH:MM:SS",
                lang.ES: "{name} debe ser una fecha y hora válida con el formato YYYY-MM-DD HH:MM:SS",
            }
        }, ptyp2)

    @staticmethod
    def mandatory(ptype: dict) -> dict:
        return DataTypes.type(ptype, {'mandatory': True})

    @staticmethod
    def optional(ptype: dict) -> dict:
        return DataTypes.type(ptype, {'mandatory': False})

    @staticmethod
    def lower(ptype: dict) -> dict:
        return DataTypes.type(ptype, {'to': 'lower'})

    @staticmethod
    def upper(ptype: dict) -> dict:
        return DataTypes.type(ptype, {'to': 'upper'})

    @staticmethod
    def default(ptype: dict, value: any) -> dict:
        return DataTypes.type(ptype, {'default': value})

    @staticmethod
    def label(ptype: dict, label: str) -> dict:
        return DataTypes.type(ptype, {'label': label})
