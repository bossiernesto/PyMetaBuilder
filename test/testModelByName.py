"""
.. module:: MetaBuilder Test
   :platform: Linux
   :synopsis: An small framework for creating builders or entities with validators. Module for processing callbacks.
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: GPL v3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>

"""
from unittest import TestCase
from PyMetabuilder import MetaBuilder


class KiteBuilder(MetaBuilder.MetaBuilder):

    KITE = 'Kite'

    def __init__(self):
        MetaBuilder.MetaBuilder.__init__(self)
        self.modelByName(self.KITE)
        self.property("design", one_of=["Indoor", "Water Kite", "Kythoon"])
        self.property("line_material", type=str)
        self.property("StringLength", type=int)


class TestKiteMetaBuilder(TestCase):

    def setUp(self):
        self.kiteBuilder = KiteBuilder()
        self.kiteBuilder.design = "Indoor"

    def testBuild(self):
        self.assertEqual(self.kiteBuilder.KITE,self.kiteBuilder.build().__class__)