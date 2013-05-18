import types
import inspect

# Type checking
def isObjOfType(obj,_type):
    return type(obj) in ([_type] + _type.__subclasses__())

def unbind(f):
    self = getattr(f, '__self__', None)
    if self is not None and not isinstance(self, types.ModuleType) \
        and not isinstance(self, type):
        if hasattr(f, '__func__'):
            return f.__func__
        return getattr(type(f.__self__), f.__name__)
    raise TypeError('not a bound method')

def bind(f, obj):
    obj.__dict__[f.__name__] = types.MethodType(f, obj, obj.__class__)

def rebind(f, obj):
    bind(unbind(f), obj)

def _makeProperty(self, propertyName, value):
    fget=lambda self: self._getProperty(propertyName)
    fset=lambda self, value: self._setProperty(propertyName, value)
    setattr(self.__class__, propertyName,property(fget, fset))
    setattr(self, self._getAttrName(propertyName), value)

class PropertyBuilder:

    def _getAttrName(self, propertyName):
        return '_'+propertyName

    def _setProperty(self, propertyName, value):
        setattr(self, self._getAttrName(propertyName), value)

    def _getProperty(self, propertyName):
        return getattr(self, self._getAttrName(propertyName))

    def _injectProperty(self,propertyName, value):
        fget = lambda self: self._getProperty(propertyName)
        fset = lambda self, value: self._setProperty(propertyName, value)
        setattr(self.__class__, propertyName,property(fget, fset))
        setattr(self, self._getAttrName(propertyName), value)

    def getPrivateMehtods(self):
        return [i for m, i in inspect.getmembers(self, predicate=inspect.ismethod) if '_' in m]

    def migrateMethods(self, target):

        methods = self.getPrivateMehtods()
        for method in methods:
            rebind(method, target)

    def buildProperties(self, target, propdict):
        if isObjOfType(propdict,dict):
            for propertName,value in propdict.iteritems():
                self.buildProperty(target, propertName, value)

    def buildProperty(self, target, propertyName, value):
        self.migrateMethods(target)
        target._injectProperty(propertyName, value)



def PropertyBuilderNoLambda(PropertyBuilder):

    def buidSetter(self,propertyName):
        getter="def get{0}(self):" \
               "    return {1}".format(propertyName,self._getAttrName(propertyName))#Armar un CodeType antes de armar el FunctionType
        types.FunctionType(getter,None,"get{0}".format(propertyName))

    def buildGetter(self,propertyName,value):
        return lambda self, value: self._setProperty(propertyName, value)

    def _injectProperty(self,propertyName, value):
        fget = self.buildGettter(propertyName)
        fset = self.builderSetter(propertyName, value)
        setattr(self.__class__, propertyName,property(fget, fset))
        setattr(self, self._getAttrName(propertyName), value)
        