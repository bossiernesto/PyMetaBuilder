"""
.. module:: MetaBuilder Callbacks
   :platform: Linux
   :synopsis: An small framework for creating builders or entities with validators. Module for processing callbacks.
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: GPL v3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>

"""
from PyMetabuilder.metaUtils import getMetaAttrName


class MetaBuilderCallbackGenerator(object):

    @staticmethod
    def processCallbacks(attribute, builder, *args, **kwargs):
        """
        Method to obtain all the callbacks and callables given a list of variable arguments.
        """
        callbacks = []
        for kwarg, validateArg in kwargs.iteritems():
            for callbackName, callback in builder._callbacks.iteritems():
                if callbackName == kwarg:
                    callbacks.append(MetaBuilderCallback(attribute, callback, validateArg))
            if hasattr(builder, kwarg):
                getattr(builder, kwarg)(attribute)
        return callbacks


class MetaBuilderCallback(object):

    def __init__(self, attribute, callback, validateArg=None):
        self.callback = callback
        self.callbackArguments = self.processCallbackArg(validateArg)
        self.callbackName = callback.__name__ + getMetaAttrName(attribute)

    def processCallbackArg(self, callbackArg):
        """
        Method to process the type of argument passed as a callback.

        :param callbackArg: value that will be passed to a callback.
        """
        calltype = type(callbackArg).__name__
        _name = {'type': lambda arg: arg.__name__, 'instancemethod': lambda arg: "'{0}'".format(arg.__name__)}
        if calltype in _name.keys():
            return _name[calltype](callbackArg)
        return callbackArg

    def generateValidator(self):
        return 'self.{0}(value,{1})'.format(self.callbackName, self.callbackArguments)