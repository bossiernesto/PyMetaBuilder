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
        self.kite =self.getKiteInstance()

    def getKiteInstance(self):
        return self.kiteBuilder.build()

    def testClass(self):
        self.assertEqual(self.kiteBuilder.KITE,self.getKiteInstance().__class__.__name__)

    def testAttributes(self):
        self.assertEqual('Indoor',self.kite.design)

    def testSetAttribute(self):
        self.kite.line_material='Linen'
        self.assertEqual('Linen',self.kite.line_material)

    def testInvalidSetAttribute(self):
        self.assertRaises(TypeError,self.kite.line_material,2)