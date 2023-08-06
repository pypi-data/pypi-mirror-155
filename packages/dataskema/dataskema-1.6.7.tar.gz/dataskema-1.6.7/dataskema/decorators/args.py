# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, C0301
import functools
from dataskema.data_schema import DataSchema


class Args(DataSchema):
    def __init__(self, data):
        super(Args, self).__init__(data)


def args(**data_schema):
    def inner_function(function):
        @functools.wraps(function)
        def arg_wrapper(**kwargs2):
            args_validator = Args(kwargs2)
            data = args_validator.validate(data_schema)
            return function(**data)
        return arg_wrapper
    return inner_function
