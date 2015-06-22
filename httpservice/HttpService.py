from enum import Enum
from flask import request


class HttpParameters(Enum):

    def __init__(self, data_type, default_value, is_optional, allowed_values, comments=''):
        """
        :param data_type:      The data type of parameter such as int, str etc.
                               will convert the parameter value string to this type on validate function
        :param allowed_values: A list of allowed values, pass None if you don't want to check this
        :param is_optional:    True-optional False-required
        :param default_value:  The default value when the parameter is not in the request url
        """
        self.__allowed_values = allowed_values
        self.__data_type = data_type
        self.__is_optional = is_optional
        self.__default_value = default_value
        self.__comments = comments

    def validate(self, value):
        """
        Validate the value to see if it match following rules:
         1. check if the value is not allowed (when allowed_values it not None)
         2. Convert the value to type data_type
        :param value:
        :return: (True/False, error reason, the value )
        """
        if self.__allowed_values is not None and value not in self.__allowed_values:
            return False, "parameter "+self.name+" value "+str(value)+" is not allowed", value
        try:
            val = self.__data_type(value)
            return True, '', val
        except Exception:
            return False, "parameter "+self.name+"value "+str(value)+" failed to convert to type "+str(self.__data_type), value

    def get_default_value(self):
        return self.__default_value

    def is_optional(self):
        return self.__is_optional

    def get_type(self):
        return self.__data_type.__name__

    def get_allowed_values(self):
        if self.__allowed_values is None:
            return ''
        else:
            return self.__allowed_values

    def get_comments(self):
        return self.__comments


def on_http_get(service):
    http_result = {}
    parameters = {}
    for parameter in service.get_parameters():
        val = request.args.get(parameter.name, None)
        if val is None:
            if parameter.is_optional():
                parameters[parameter.name] = parameter.get_default_value()
            else:
                http_result['code'] = 1
                http_result['error'] = 'Missing parameter '+parameter.name
                return http_result
        else:
            (pass_validate, reason, value) = parameter.validate(val)
            if pass_validate:
                parameters[parameter.name] = value
            else:
                http_result['code'] = 1
                http_result['error'] = reason
                return http_result
    return service.on_get(parameters)