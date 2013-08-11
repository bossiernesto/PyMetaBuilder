"""
.. module:: MetaBuilder Core
   :platform: Linux
   :synopsis: An small framework for creating builders or entities with validators. Module for processing callbacks.
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: GPL v3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>

"""

class MetaBuilderCallback(object):

    def __init__(self, callbackName, callbackArguments):
        self.callbackName = callbackName
        self.callbackArguments = callbackArguments
