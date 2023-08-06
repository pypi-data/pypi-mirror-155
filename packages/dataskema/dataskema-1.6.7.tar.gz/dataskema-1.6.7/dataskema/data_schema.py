# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, C0301
from dataskema.validator import SchemaValidator
from dataskema.validator import SchemaValidationFailure
from dataskema.validator import SchemaFormatError
from dataskema.validator import KEYWORD_MESSAGE, KEYWORD_LABEL, KEYWORD_IS_VALID
from dataskema import lang
from dataskema import util

MAX_VALIDATION_MESSAGES = 1


class SchemaValidationResult(Exception):

    def __init__(self, message: str, results: dict):
        idx = message.find('\n')
        line = message[0:idx] if idx >= 0 else message
        line = util.no_acute(line)
        super(SchemaValidationResult, self).__init__(line)
        self.message = message
        self.results = results if results is not None else {}

    def get_results(self) -> dict:
        return self.results

    def get_result_of(self, name: str) -> dict:
        return self.results.get(name)

    def get_message(self) -> str:
        return self.message

    def get_messages(self) -> list:
        messages = []
        for item in self.results.values():
            if isinstance(item, dict):
                label = item.get(KEYWORD_LABEL)
                msg = item.get(KEYWORD_MESSAGE)
                if msg is not None:
                    messages.append(f"{label}: {msg}")
        return messages


class DataSchema:

    def __init__(self, data: dict):

        """
        """
        if not isinstance(data, dict):
            dtype = util.typeof(data)
            raise SchemaFormatError(f"Only named parameters must be passed to DataScheme. Found '{dtype}'", {})
        self.data = dict(data)

    def validate(self, data_schema: dict) -> dict:
        """
        Validate the incoming data with this data schema
        :param data_schema: data schema
        :return: validation result {
            <named-field>: {
                label: <string> -> Label defined for this field
                is_valid: <bool> -> If was validated or not
                message: <string> -> Validation message for this named field. Only if is_valid=False
            },
            '_result': { -> Special named field for general
                message: <string> -> Showing first validation message with total rest of messages
            }
        }
        """
        # -- incluye los datos por defecto
        for dname, ddict in data_schema.items():
            if self.data.get(dname) is None:
                self.data[dname] = None

        valid = True
        result = {}
        first_messages = []
        total_errors = 0
        for pname, pvalue in self.data.items():
            schema = data_schema.get(pname)
            if schema is None or not isinstance(schema, dict):
                _add_is_not_valid(result, pname, pname, f"'{pname}' has not data-scheme definition")
                continue
            validator = SchemaValidator(schema)
            try:
                pvalue = validator.validate(pname, pvalue)
                self.data[pname] = pvalue
                _add_is_valid(result, pname)
            except SchemaValidationFailure as ex:
                _add_is_not_valid(result, pname, ex.get_name(), ex.get_message(True))
                if MAX_VALIDATION_MESSAGES <= 0 or len(first_messages) < MAX_VALIDATION_MESSAGES:
                    first_messages.append(ex.get_message(False))
                valid = False
                total_errors = total_errors + 1
        if not valid:
            first_message = '\n'.join(first_messages) + '\n' + lang.get_more_messages(total_errors - 1)
            raise SchemaValidationResult(first_message, result)
        return self.data


def _add_is_not_valid(result: dict, name: str, label: str, message: str):
    result[name] = {
        KEYWORD_IS_VALID: False,
        KEYWORD_LABEL: label,
        KEYWORD_MESSAGE: message
    }


def _add_is_valid(result: dict, name: str):
    result[name] = {
        KEYWORD_IS_VALID: True,
    }

