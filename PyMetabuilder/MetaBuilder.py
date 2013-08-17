"""
.. module:: MetaBuilder Core
   :platform: Linux
   :synopsis: An small framework for creating builders or entities with validators. Core business module.
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: GPL v3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>

"""
from types import MethodType
from PyMetabuilder.metaUtils import *
from PyMetabuilder.MetaBuilderMutator import *
from PyMetabuilder.MetaBuilderCallbacks import *

class MetaBuilder(object):
    """

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
        if not type(value) in ([expected_type]):
            raise TypeError("Should be of type {0}".format(expected_type))

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
            raise ValidatorError("Length of {0} was not the expected one of {1}".format(value,expected_length))

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
        self.customMethodValidator(value, methodCall)

    def customMethodValidator(self, value, method):
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

    def modelByName(self,className):
        self.klass = type(className, (), {})
        self.model(self.klass)

    def model(self, klass):
        """
        Method to set the class type to build.

        :param klass: Class to build instances from it.
        """
        createvarIfNotExists(self, "_model", klass)
        self._model = klass

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
        callbacks = MetaBuilderCallbackGenerator.processCallbacks(attribute, self, *args, **kwargs)
        if len(callbacks) > 0:
            for callback in callbacks:
                setattr(self, callback.callbackName, MethodType(unbind(callback.callback), self))
            #create setter and getters
            self.mutator.buildProperty(self, attribute, callbacks)
        else:
            self.mutator.buildProperty(self, attribute, None)
        self._properties.append(attribute)

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
            isAttributeDefined(self, required)
        klass = get_class(self._model.__module__ + '.' + self._model.__name__)
        instance = klass()
        for prop in self.properties():
            for method in [getattr(self, m) for m in getMethodsByName(self, prop)]:
                if self._prefix in method.__name__:
                    setattr(instance, method.__name__ + getMetaAttrName(prop), MethodType(unbind(method), self))
                else:
                    setattr(instance, method.__name__, getattr(self, method.__name__))
            getter = getattr(instance, 'get{0}'.format(prop))
            setter = getattr(instance, 'set{0}'.format(prop))
            self.mutator.setProperty(instance, prop, getter, setter, getattr(self, getMetaAttrName(prop)))
        return instance


class OptionValueError(Exception):
    pass


class ValidatorError(Exception):
    pass


class MetaBuilderError(Exception):
    pass
