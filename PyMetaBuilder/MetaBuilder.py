from types import MethodType, ModuleType
import string


def getMethodsByName(obj, name):
    return [method for method in getMethods(obj) if name in method]


def get_class(klass):
    parts = klass.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def bind(f, obj):
    obj.__dict__[f.__name__] = MethodType(f, obj, obj.__class__)

rebind = lambda f, obj: bind(unbind(f), obj)


def getMethods(obj):
    ret = []
    for e in dir(obj):
        try:
            if callable(getattr(obj, e)):
                ret.append(e)
        except AttributeError:
            pass
    return ret


def isAttributeDefined(obj, attribute):
    if hasattr(obj, attribute) and getattr(obj, attribute) is not None:
        return
    raise AttributeError('Attribute {0} is not defined'.format(attribute))


def getAttributes(obj):
    return [prop for (prop, value) in vars(obj).iteritems()]


def createvarIfNotExists(obj, var, initial):
    try:
        getattr(obj, var)
    except AttributeError:
        setattr(obj, var, initial)


def unbind(f):
    self = getattr(f, '__self__', None)
    if self is not None and not isinstance(self, ModuleType) and not isinstance(self, type):
        if hasattr(f, '__func__'):
            return f.__func__
        return getattr(type(f.__self__), f.__name__)
    raise TypeError('not a bound method')


class MetaBuilder(object):

    def __init__(self):
        self.prefix = 'validate_'
        self.validators = self._get_Validators()
        self.callbacks = dict()
        for v in self.validators:
            self.callbacks[v.split(self.prefix)[1]] = getattr(self, v)
        self.start = ['start', '_model', '_required_args']+ getAttributes(self)

    #Validators
    def _get_Validators(self):
        return getMethodsByName(self, self.prefix)

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
        except TypeError, e:
            raise ValidatorError(e, 'Problem calling method {0}'.format(method))

    def required(self, *args, **kwargs):
        self._required_args = []
        for arg in args:
            self._required_args.append(arg)

    def model(self, klass):
        createvarIfNotExists(self, "_model", klass)
        self._model = klass

    def property(self, attribute, *args, **kwargs):
        """
        self.property('age',type=int)
        """
        callback = self.getCallback(*args, **kwargs)
        if callback:
            callbackName = callback.__name__+'_'+attribute
            self.__dict__[callbackName] = MethodType(unbind(callback), self)
            callbackarg = self.getCallbackArg(callbackName, *args, **kwargs)
            #create setter and getters
            self.buildProperty(attribute, callbackName, callbackarg)
        else:
            self.buildProperty(attribute, None, None)

    def buildProperty(self, attributeName, callbackName=None, callbackarg=None):
        getter = self.buildGetter(attributeName)
        setter = self.buildSetter(attributeName, callbackName, callbackarg)
        self.setProperty(self, attributeName, getter, setter, None)

    def setProperty(self, obj, attributeName, getter, setter, defaultValue=None):
        setattr(obj.__class__, attributeName, property(fget=getter, fset=setter))
        setattr(obj, '_'+attributeName, defaultValue)

    def getSignatureString(self, methodString):
        return methodString[methodString.find("def")+3:methodString.find("(")].strip()

    def _getAttrName(self, propertyName):
        return '_'+propertyName

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
        dict = {}
        methodName = self.getSignatureString(code)
        exec code.strip() in dict
        klass.__dict__[methodName] = dict[methodName]
        return klass.__dict__[methodName]

    def getCallback(self, *args, **kwargs):
        for kwarg, validateArg in kwargs.iteritems():
            for callbackname, callback in self.callbacks.iteritems():
                if callbackname == kwarg:
                    return callback
            return None

    def getCallbackArg(self, callbackName, *args, **kwargs):
        argumentName, argument = kwargs.popitem()
        _name = {'type': lambda arg: arg.__name__, 'validates': lambda arg: "'{0}'".format(arg.__name__)}
        for n, a in _name.iteritems():
            if n in callbackName:
                return a(argument)
        return argument

    def getProperties(self):
        return [string.replace(k, '_', '') for k in getAttributes(self) if k not in getMethods(self)+self.start]

    def build(self):
        for required in self._required_args:
            isAttributeDefined(self, required)
        klass = get_class(self._model.__module__+'.'+self._model.__name__)
        instance = klass()
        for prop in self.getProperties():
            for method in [getattr(self, m) for m in getMethodsByName(self, prop)]:
                if self.prefix in method.__name__:
                    instance.__dict__[method.__name__+'_'+prop] = MethodType(unbind(method), self)
                else:
                    instance.__dict__[method.__name__] = self.__dict__[method.__name__]
            getter = getattr(instance, 'get{0}'.format(prop))
            setter = getattr(instance, 'set{0}'.format(prop))
            self.setProperty(instance, prop, getter, setter, getattr(self, '_'+prop))
        return instance


class OptionValueError(StandardError):
    pass


class ValidatorError(StandardError):
    pass
