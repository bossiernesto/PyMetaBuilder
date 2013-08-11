"""
.. module:: MetaBuilder Core
   :platform: Linux
   :synopsis: An small framework for creating builders or entities with validators. Mutator class for creating properties.
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: GPL v3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>

"""
from metaUtils import getMetaAttrName
from types import ModuleType


def unbind(f):
    """
    Function that unbinds a given function if it's actually binded to an object. If it's not binded to an object it'll
    raise a TypeError Exception

    :param f: function to unbind from an object
    :type f: function
    :raises: TypeError
    """
    self = getattr(f, '__self__', None)
    if self is not None and not isinstance(self, ModuleType) and not isinstance(self, type):
        if hasattr(f, '__func__'):
            return f.__func__
        return getattr(type(f.__self__), f.__name__)
    raise TypeError('not a bound method')


class MetaBuilderMutator(object):
    """

    """

    def getSignatureString(self, methodString):
        """

        """
        return methodString[methodString.find("def") + 3:methodString.find("(")].strip()

    def buildProperty(self, instance, attributeName, callbackName=None, callbackarg=None):
        """
        Method that given an instance and an attributeName will generate the property getter and setter for that
        attribute and associate to the instance.

        :param instance: instance that will be associated the property methods
        :type instance: <type 'instance'>
        :param attributeName: then name of the attribute that will be associated the property methods for the instance
        :type attributeName: str
        """
        getter = self.buildGetter(instance, attributeName)
        setter = self.buildSetter(instance, attributeName, callbackName, callbackarg)
        self.setProperty(instance, attributeName, getter, setter, None)

    def setProperty(self, obj, attributeName, getter, setter, defaultValue=None):
        """

        """
        setattr(obj.__class__, attributeName, property(fget=getter, fset=setter))
        setattr(obj, getMetaAttrName(attributeName), defaultValue)


    def buildGetter(self, instance, propertyName):
        """
        Method that given an instance and a propertyName, builds a getter dynamically and associate this propertyName
        to the instance.

        :param instance: The instance to associate the getter method
        :type instance: <type 'instance'>
        :param propertyName: The property that the getter will return on calling
        :type propertyName: str
        """
        getter = "def get{0}(self):\n" \
                 "    return self.{1}".format(propertyName, getMetaAttrName(propertyName))
        return self.createFunction(instance, getter)

    def buildSetter(self, instance, propertyName, callbackName=None, callbackarg=None):
        """
        Method that given an instance and a propertyName, builds a setter dynamically and associate this propertyName
        to the instance. Will append validators if any callback passed

        :param instance: The instance to associate the getter method
        :type instance: <type 'instance'>
        :param propertyName: The property that the getter will return on calling
        :type propertyName: str
        """
        callback = '' if callbackName is None else 'self.{0}(value,{1})'.format(callbackName, callbackarg)
        setter = "def set{0}(self,value):\n" \
                 "    {1}\n" \
                 "    self.{2}=value".format(propertyName, callback.strip(), getMetaAttrName(propertyName))
        return self.createFunction(instance, setter)

    def createFunction(self, instance, code):
        """
        Method to create a function/method given a code in python and set it to a given instance.

        :param instance: object to set the code given in the parameters of this method
        :type instance: <type 'instance'>
        :param code: String containing the code to set to the object
        :type code: str
        """
        method_dict = {}
        methodName = self.getSignatureString(code)
        exec(code.strip(), globals(), method_dict)
        setattr(instance, methodName, method_dict[methodName])
        return instance.__dict__[methodName]