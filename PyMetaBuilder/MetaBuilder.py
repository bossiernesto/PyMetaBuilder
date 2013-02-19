__author__ = 'b03418'

def getMethods(obj):
    return [e for e in dir(obj) if callable(getattr(obj, e))]

def getAttributes(obj):
    return [prop for (prop,value) in vars(obj).iteritems()]


class MetaBuilder:

    #Validators

    def validate_type (self,value,expected_type):
        if not type(value) in ([expected_type] + expected_type.__subclasses__()):
            raise TypeError,"Should be of type %s" % expected_type

    def validate_optionvalues(self,value,options):
        if value not in options:
            raise OptionValueError,"Value %s not in expected options" % value

    def validate_customMethod(self,value,method):
        if not callable(method):
            raise TypeError,"%s is not a method or callable one" % method
        try:
            if not method(value):
                raise ValidatorError,"Value %s did not passed validation %s"  % (value,method)
        except TypeError,e:
            raise ValidatorError,e,'Problem calling method %s' % method

    def required(self,*args,**kwargs):
        self._required_args=[]
        for arg in args:
            self._required_args.append(arg)

    def model(self,klass):
        self._model=klass

    @property
    def property(self,attribute,*args,**kwargs):
            pass

    property


class OptionValueError(StandardError):
    def __init__(self, *args, **kwargs):
        StandardError.__init__(self, *args, **kwargs)

class ValidatorError(StandardError):
    def __init__(self, *args, **kwargs):
        StandardError.__init__(self, *args, **kwargs)
