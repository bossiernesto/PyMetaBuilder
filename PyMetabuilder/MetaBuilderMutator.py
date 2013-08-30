"""
.. module:: MetaBuilder Mutator
   :platform: Linux
   :synopsis: An small framework for creating builders or entities with validators. Mutator class for creating properties.
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: GPL v3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>

"""
from types import ModuleType, MethodType
from PyMetabuilder.metaUtils import getMeta_attr_name,getMethodsByName

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

    def get_signature_string(self, methodString):
        """

        """
        return methodString[methodString.find("def") + 3:methodString.find("(")].strip()

    def build_property(self, instance, attributeName, callbacks=None):
        """
        Method that given an instance and an attributeName will generate the property getter and setter for that
        attribute and associate to the instance.

        :param instance: instance that will be associated the property methods
        :type instance: <type 'instance'>
        :param attributeName: then name of the attribute that will be associated the property methods for the instance
        :type attributeName: str
        """
        getter = self.build_getter(instance, attributeName)
        setter = self.build_setter(instance, attributeName, callbacks)
        self.set_property(instance, attributeName, getter, setter, None)

    def set_property(self, obj, attributeName, getter, setter, defaultValue=None):
        """

        """
        setattr(obj.__class__, attributeName, property(fget=getter, fset=setter))
        setattr(obj, getMeta_attr_name(attributeName), defaultValue)

    def build_getter(self, instance, propertyName):
        """
        Method that given an instance and a propertyName, builds a getter dynamically and associate this propertyName
        to the instance.

        :param instance: The instance to associate the getter method
        :type instance: <type 'instance'>
        :param propertyName: The property that the getter will return on calling
        :type propertyName: str
        """
        getter = "def get{0}(self):\n" \
                 "    return self.{1}".format(propertyName, getMeta_attr_name(propertyName))
        return self.create_function(instance, getter)

    def build_setter(self, instance, propertyName, callbacks=None):
        """
        Method that given an instance and a propertyName, builds a setter dynamically and associate this propertyName
        to the instance. Will append validators if any callback passed

        :param instance: The instance to associate the getter method
        :type instance: <type 'instance'>
        :param propertyName: The property that the getter will return on calling
        :type propertyName: str
        """
        callback = '' if callbacks is None else '\n'.join('\t'+callback.generate_validator().strip() for callback in callbacks)
        setter = "def set{0}(self,value):\n" \
                 "{1}\n" \
                 "\tself.{2}=value".format(propertyName, callback, getMeta_attr_name(propertyName))
        return self.create_function(instance, setter)

    def create_function(self, instance, code):
        """
        Method to create a function/method given a code in python and set it to a given instance.

        :param instance: object to set the code given in the parameters of this method
        :type instance: <type 'instance'>
        :param code: String containing the code to set to the object
        :type code: str
        """
        method_dict = {}
        methodName = self.get_signature_string(code)
        exec(code.strip(), globals(), method_dict)
        setattr(instance, methodName, method_dict[methodName])
        return instance.__dict__[methodName]

    def migrate_attribute(self, property, metabuilder, instance):
        """
        Method migrate an attribute from the metabuilder instance to the instance created by itself.

        :param property: object to set the code given in the parameters of this method
        :type property: <type 'property'>
        :param metabuilder: instance of a metabuilder where to extract the methods and validators of the attribute to
        migrate
        :type metabuilder: <type 'Metabuilder'>
        :param instance: instance created that will hold the property and the validators
        :type instance: <type 'instance'>
        """
        for method in [getattr(metabuilder, m) for m in getMethodsByName(metabuilder, property)]:
            if metabuilder._prefix in method.__name__:
                setattr(instance, method.__name__ + getMeta_attr_name(property), MethodType(unbind(method), metabuilder))
            else:
                setattr(instance, method.__name__, getattr(metabuilder, method.__name__))
        getter = getattr(instance, 'get{0}'.format(property))
        setter = getattr(instance, 'set{0}'.format(property))
        self.set_property(instance, property, getter, setter, getattr(metabuilder, getMeta_attr_name(property)))