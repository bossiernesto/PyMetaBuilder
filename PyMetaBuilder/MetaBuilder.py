from types import MethodType, ModuleType
from metaUtils import *


def unbind(f):
    self = getattr(f, '__self__', None)
    if self is not None and not isinstance(self, ModuleType) and not isinstance(self, type):
        if hasattr(f, '__func__'):
            return f.__func__
        return getattr(type(f.__self__), f.__name__)
    raise TypeError('not a bound method')


class MetaBuilder(object):

    def __init__(self):
        self._prefix = 'validate_'
        self._validators = self._get_Validators()
        self._callbacks = dict()
        for v in self._validators:
            self._callbacks[v.split(self._prefix)[1]] = getattr(self, v)
        self._properties = []
        self._required_args = []
        self._reserved = getAttributes(self) + ['_model']

    isReserved = lambda self, prop: prop in self._reserved

    #Validators
    def _get_Validators(self):
        return getMethodsByName(self, self._prefix)

    def _getValidatorsByName(self, name):
        return [getattr(self, val) for val in self._get_Validators() if name in val]

    def validate_type(self, value, expected_type):
        if not type(value) in ([expected_type]):
            raise TypeError("Should be of type {0}".format(expected_type))

    def validate_one_of(self, value, options):
        if value not in options:
            raise OptionValueError("Value {0} not in expected options".format(value))

    def validate_validates(self, value, method):
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
        for arg in args:
            self._required_args.append(arg)

    def model(self, klass):
        createvarIfNotExists(self, "_model", klass)
        self._model = klass

    def property(self, attribute, *args, **kwargs):
        """
        self.property('age',type=int)
        """
        if self.isReserved(attribute):
            raise MetaBuilderError("Attribute name {0} is a reserved word".format(attribute))
        callback, callbackarg = self.getCallback(*args, **kwargs)
        if callback:
            callbackName = callback.__name__ + self._getAttrName(attribute)
            setattr(self, callbackName, MethodType(unbind(callback), self))
            #create setter and getters
            self.buildProperty(attribute, callbackName, callbackarg)
        else:
            self.buildProperty(attribute, None, None)
        self._properties.append(attribute)

    def buildProperty(self, attributeName, callbackName=None, callbackarg=None):
        getter = self.buildGetter(attributeName)
        setter = self.buildSetter(attributeName, callbackName, callbackarg)
        self.setProperty(self, attributeName, getter, setter, None)

    def setProperty(self, obj, attributeName, getter, setter, defaultValue=None):
        setattr(obj.__class__, attributeName, property(fget=getter, fset=setter))
        setattr(obj, self._getAttrName(attributeName), defaultValue)

    def getSignatureString(self, methodString):
        return methodString[methodString.find("def") + 3:methodString.find("(")].strip()

    def _getAttrName(self, propertyName):
        return '_' + propertyName

    def buildGetter(self, propertyName):
        getter = "def get{0}(self):\n" \
                 "    return self.{1}".format(propertyName, self._getAttrName(propertyName))
        return self.createFunction(self, getter)

    def buildSetter(self, propertyName, callbackName=None, callbackarg=None):
        callback = '' if callbackName is None else 'self.{0}(value,{1})'.format(callbackName, callbackarg)
        setter = "def set{0}(self,value):\n" \
                 "    {1}\n" \
                 "    self.{2}=value".format(propertyName, callback.strip(), self._getAttrName(propertyName))
        return self.createFunction(self, setter)

    def createFunction(self, klass, code):
        method_dict = {}
        methodName = self.getSignatureString(code)
        exec(code.strip(), globals(), method_dict)
        setattr(klass, methodName, method_dict[methodName])
        return klass.__dict__[methodName]

    def getCallback(self, *args, **kwargs):
        for kwarg, validateArg in kwargs.iteritems():
            for callbackname, callback in self._callbacks.iteritems():
                if callbackname == kwarg:
                    return callback, self.processCallbackArg(validateArg)
        return None, None

    def processCallbackArg(self, callbackArg):
        calltype = type(callbackArg).__name__
        _name = {'type': lambda arg: arg.__name__, 'instancemethod': lambda arg: "'{0}'".format(arg.__name__)}
        if calltype in _name.keys():
            return _name[calltype](callbackArg)
        return callbackArg

    def properties(self):
        return self._properties

    def build(self):
        for required in self._required_args:
            isAttributeDefined(self, required)
        klass = get_class(self._model.__module__ + '.' + self._model.__name__)
        instance = klass()
        for prop in self.properties():
            for method in [getattr(self, m) for m in getMethodsByName(self, prop)]:
                if self._prefix in method.__name__:
                    setattr(instance, method.__name__ + self._getAttrName(prop), MethodType(unbind(method), self))
                else:
                    setattr(instance, method.__name__, getattr(self, method.__name__))
            getter = getattr(instance, 'get{0}'.format(prop))
            setter = getattr(instance, 'set{0}'.format(prop))
            self.setProperty(instance, prop, getter, setter, getattr(self, self._getAttrName(prop)))
        return instance


class OptionValueError(Exception):
    pass


class ValidatorError(Exception):
    pass


class MetaBuilderError(Exception):
    pass
