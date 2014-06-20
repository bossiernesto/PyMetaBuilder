"""
.. module:: MetaBuilder Credit Card Test
   :platform: Linux
   :synopsis: An small framework for creating builders or entities with validators. Test for version version >=0.15.
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: GPL v3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>

"""
from unittest import TestCase
from PyMetabuilder import MetaBuilder


class Logo:
    pass


class CreditCard:
    pass


class CreditCardMetaBuilder(MetaBuilder):

    def __init__(self):
        MetaBuilder.__init__(self)
        self.model(CreditCard)
        self.property("ccnumber", type=str, length=16, required=True)
        self.property("ccName", type=str, required=True)
        self.property("extraLogo", type=Logo)


class TestCreditCardMetaBuilder(TestCase):

    def setUp(self):
        self.cardBuilder = CreditCardMetaBuilder()

    def CCBuild(self):
        creditcard = self.cardBuilder.build()

    def test_normal_build(self):
        self.cardBuilder.ccnumber = "5430422223333444"
        self.cardBuilder.ccName = 'John Doe'
        self.cardBuilder.build()

    def test_attr_error_build(self):
        self.cardBuilder.ccnumber = "5430422223333444"
        self.assertRaises(AttributeError,self.cardBuilder.build)

    def test_invalid_length_build(self):
        self.assertRaises(ValidatorError,self.cardBuilder.ccnumber,"543042222333444")