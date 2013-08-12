"""
.. module:: MetaBuilder Utils
   :platform: Linux
   :synopsis: An small framework for creating builders or entities with validators. useful and introspective functions.
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: GPL v3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>

"""


def getMethodsByName(p_object, name):
    return [method for method in getMethods(p_object) if name in method]


def get_class(klass):
    parts = klass.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


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


def getMetaAttrName(propertyName):
    return '_' + propertyName