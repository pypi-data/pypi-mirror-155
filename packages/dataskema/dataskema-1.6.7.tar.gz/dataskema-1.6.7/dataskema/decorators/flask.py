# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, C0301
import json
import functools
from dataskema.data_schema import DataSchema, SchemaValidationResult
from flask import request, make_response, Response


class JSON(DataSchema):
    def __init__(self):
        super(JSON, self).__init__(request.get_json())


class Query(DataSchema):
    def __init__(self):
        super(Query, self).__init__(request.args)


class InUrl(DataSchema):
    def __init__(self, data):
        super(InUrl, self).__init__(data)


def flask_json(**kwargs):
    def inner_function(function):
        @functools.wraps(function)
        def wrapper(**data):
            json_validator = JSON()
            outdata = json_validator.validate(kwargs)
            outdata.update(data)
            return function(**outdata)
        return wrapper
    return inner_function


def flask_query(**kwargs):
    def inner_function(function):
        @functools.wraps(function)
        def wrapper(**data):
            query_validator = Query()
            outdata = query_validator.validate(kwargs)
            outdata.update(data)
            return function(**outdata)
        return wrapper
    return inner_function


def __normalize_escaped_codes(pvalue: str) -> str:
    pvalue = pvalue.replace('${slash}', '/')
    pvalue = pvalue.replace('${backslash}', '\\')
    return pvalue


def flask_url(**data_schema):
    def inner_function(function):
        @functools.wraps(function)
        def arg_wrapper(**kwargs2):
            for key in kwargs2.keys():
                if isinstance(kwargs2[key], str):
                    kwargs2[key] = __normalize_escaped_codes(kwargs2[key])
            args_validator = InUrl(kwargs2)
            data = args_validator.validate(data_schema)
            return function(**data)
        return arg_wrapper
    return inner_function
