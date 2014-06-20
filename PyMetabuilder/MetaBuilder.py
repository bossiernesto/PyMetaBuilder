"""
.. module:: MetaBuilder Core
   :platform: Linux
   :synopsis: An small framework for creating builders or entities with validators. Core business module.
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: GPL v3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>

"""
from PyMetabuilder.metaUtils import *
from PyMetabuilder.MetaBuilderMutator import *
from PyMetabuilder.MetaBuilderCallbacks import *

class MetaBuilder(object):
    """
    This is the base class that should inherit any builder the user wants to code to get instances via validations
    """

    def __init__(self):
        self._prefix = 'validate_'
        self._validators = self._get_Validators()
        self._callbacks = dict()
        for v in self._validators:
            self._callbacks[v.split(self._prefix)[1]] = getattr(self, v)
        self._properties = []
        self._required_args = []
        self._reserved = getAttributes(self) + ['_model']
        self.mutator = MetaBuilderMutator()

    isReserved = lambda self, prop: prop in self._reserved

    #Validator methods
    def _get_Validators(self):
        """
        Method for getting the current validators of the module. Returns list with the validators names.
        """
        return getMethodsByName(self, self._prefix)

    def _getValidatorsByName(self, name):
        """
        Method for getting the validators that matches a name or pattern given.

        :param name: name of the pattern to filter
        :type name: str
        """
        return [getattr(self, val) for val in self._get_Validators() if name in val]

    def validate_type(self, value, expected_type):
        """
        validation of the type to a value to set. Raises TypeError when the type of value is not the one of
        expected_value.

        :param value: value to validate type
        :param expected_type: Type to test with the type of the value given in the parameters
        :type expected_type: type
        :raises: TypeError
        """
        expected_types = expected_type if isinstance(expected_type, list) else [expected_type]
        if not type(value) in expected_types:
            raise TypeError("{0} Should be of type {1}".format(value, expected_type))

    def validate_length(self, value, expected_length):
        """
        Validation of the length of a value to set. Raises ValidatorError if expected length is not equal to the actual
        length of the value.

        :param value: value to validate length
        :param expected_length: expected length to validate
        :type expected_length: int
        :raises: ValidatorError
        """
        if not len(value) == expected_length:
            raise ValidatorError("Length of {0} was not the expected one of {1}".format(value, expected_length))

    def validate_one_of(self, value, options):
        """
        Validation that checks that a value is one of the options given as parameter. Raises OptionValueError if the
        value to set is not in the options list.

        :param value: value to check
        :param options: List of valid values that the value parameter should have.
        :type options: List
        :raises: OptionValueError
        """
        if value not in options:
            raise OptionValueError("Value {0} not in expected options".format(value))

    def validate_validates(self, value, method):
        """
        Method to set a custom validator given by parameter that will check a value to set. Raises TypeError if there's
        a problem calling the validator or TypeError if the method parameter is not callable.
        Will raise a ValidatorError if the custom validation against the value fails.

        :param value: value to set.
        :param method: Custom validator to test
        :type method: Method
        :raises: TypeError,ValidatorError,TypeError
        """
        methodCall = getattr(self, method)
        self.custom_method_validator(value, methodCall)

    def custom_method_validator(self, value, method):
        if not callable(method):
            raise TypeError("{0} is not a method or callable one".format(method))
        try:
            if not method(value):
                raise ValidatorError("Value {0} did not passed validation {1}".format(value, method))
        except TypeError:
            raise ValidatorError('Problem calling method {0}'.format(method))

    def required(self, *args, **kwargs):
        """
        Method to set one or more attributes as required. This will ensure that when an instance of the builder is built
        the framework will check that these required arguments have been previously set.

        :param args: variable arguments to append to the required list.
        """
        for arg in args:
            self._required_args.append(arg)

    def model_by_name(self, className):
        self.klass = type(className.title(), (), {})
        self.model(self.klass)
        return self

    def model(self, klass):
        """
        Method to set the class type to build.

        :param klass: Class to build instances from it.
        """
        createvar_if_not_exists(self, "_model", klass)
        self._model = klass
        return self

    def property(self, attribute, *args, **kwargs):
        """
        Method to define a property for the instances to be created. Given an attribute name and variable validators or
        properties, the framework will create a property for that name and will give it the properties given also as
        parameter. These properties will be still valid in the instances created.

        :param attribute: attribute name to be created.
        :type attribute: str
        :param kwargs: arguments of the validators and aspects that will be bind to the property
        :raises: MetaBuilderError
        """
        if self.isReserved(attribute):
            raise MetaBuilderError("Attribute name {0} is a reserved word".format(attribute))
        validators = GeneratorOfValidations.process_validators(attribute, self, *args, **kwargs)
        if len(validators) > 0:
            for validator in validators:
                setattr(self, validator.validatorName, MethodType(unbind(validator.validator), self))
                #create setter and getters
            self.mutator.build_property(self, attribute, validators)
        else:
            self.mutator.build_property(self, attribute, None)
        self._properties.append(attribute)
        return self

    def properties(self):
        """
        Method to get the properties set so far. This list of properties will be the one assigned to the instance when
        it's built.
        """
        return self._properties

    def build(self):
        """
        Method to finally build an instance given the fact that some properties with or without validators have been
        defined and set. Raises AttributeError if an propertied defined as required has not been set properly.

        :raises: AttributeError
        """
        for required in self._required_args:
            is_attribute_defined(self, required)
        try:
            klass = get_class(self._model.__module__ + '.' + self._model.__name__)
            instance = klass()
        except AttributeError:
            #if fails then class has been generated dinamically in this module
            instance = self._model()
        for prop in self.properties():
            self.mutator.migrate_attribute(prop, self, instance)
        return instance


class OptionValueError(Exception):
    pass


class ValidatorError(Exception):
    pass


class MetaBuilderError(Exception):
    pass
