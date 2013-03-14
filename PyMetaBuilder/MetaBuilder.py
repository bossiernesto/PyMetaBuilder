def getMethods(obj):
    return [e for e in dir(obj) if callable(getattr(obj, e))]

def getAttributes(obj):
    return [prop for (prop,value) in vars(obj).iteritems()]

def createvar_if_not_exists(obj,var,initial):
    try:
        getattr(obj,var)
    except AttributeError:
        setattr(obj,var,initial)

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
        createvar_if_not_exists(self,"_model",klass)
        self._model=klass

    def property(self,attribute,**kwargs):
        self.build_validator('validate_{0}'.format(attribute),kwargs)
        def setAttribute(self, propertyValue):
            self.value[attribute] = propertyValue
        def getAttribute(self):
            return self.value[attribute]
        setattr(self.__class__, 'set'+ attribute.capitalize(), setAttribute)
        setattr(self.__class__, 'get'+ attribute.capitalize(), getAttribute)



class OptionValueError(StandardError):
    def __init__(self, *args, **kwargs):
        StandardError.__init__(self, *args, **kwargs)

class ValidatorError(StandardError):
    def __init__(self, *args, **kwargs):
        StandardError.__init__(self, *args, **kwargs)
