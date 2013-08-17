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


class CreditCardMetaBuilder(MetaBuilder.MetaBuilder):

    def __init__(self):
        MetaBuilder.MetaBuilder.__init__(self)
        self.model(CreditCard)
        self.property("ccnumber", type=str, length=16, required=True)
        self.property("ccName", type=str, required=True)
        self.property("extraLogo", type=Logo)


class TestCreditCardMetaBuilder(TestCase):

    def setUp(self):
        self.cardBuilder = CreditCardMetaBuilder()

    def testBuild(self):
        creditcard = self.cardBuilder.build()

    def testExceptionBuild(self):
        self.cardBuilder.ccnumber = "43042222333344"
        self.cardBuilder.build()
