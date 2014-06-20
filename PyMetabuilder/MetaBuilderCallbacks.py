"""
.. module:: MetaBuilder Validator Module
   :platform: Linux
   :synopsis: An small framework for creating builders or entities with validators. Module for processing callbacks.
   :copyright: (c) 2013-14 by Ernesto Bossi.
   :license: GPL v3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>

"""
from PyMetabuilder.metaUtils import getMeta_attr_name
import six

class GeneratorOfValidations(object):

    @staticmethod
    def process_validators(attribute, builder, *args, **kwargs):
        """
        Method to obtain all the validators and callables given a list of variable arguments.
        """
        validators = []
        for kwarg, validateArg in six.iteritems(kwargs):
            for callbackName, callback in six.iteritems(builder._callbacks):
                if callbackName == kwarg:
                    validators.append(MetaBuilderValidator(attribute, callback, validateArg))
            if hasattr(builder, kwarg):
                getattr(builder, kwarg)(attribute)
        return validators


class MetaBuilderValidator(object):

    def __init__(self, attribute, validator, validateArg=None):
        self.validator = validator
        self.validatorArguments = self.process_validator_arg(validateArg)
        self.validatorName = validator.__name__ + getMeta_attr_name(attribute)

    def process_validator_arg(self, validatorArg):
        """
        Method to process the type of argument passed as a callback.

        :param validatorArg: value that will be passed to a callback.
        """
        calltype = type(validatorArg).__name__
        _name = {'type': lambda arg: arg.__name__, 'instancemethod': lambda arg: "'{0}'".format(arg.__name__),
                 'method': lambda arg: "'{0}'".format(arg.__name__)}
        if calltype in _name.keys():
            return _name[calltype](validatorArg)
        return validatorArg

    def generate_validator(self):
        return 'self.{0}(value,{1})'.format(self.validatorName, self.validatorArguments)