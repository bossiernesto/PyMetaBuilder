"""
.. module:: MetaBuilder Core
   :platform: Linux
   :synopsis: An small framework for creating builders or entities with validators. Test for version version >=0.14.
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: GPL v3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>

"""
from PyMetaBuilder.MetaBuilder import MetaBuilder
from unittest import TestCase, skip


class Logo:
    pass


class CreditCard:
    pass


class CreditCardMetaBuilder(MetaBuilder):

    def __init__(self):
        MetaBuilder.__init__(self)
        self.model(CreditCard)
        self.property("ccnumber", type=int, required=True, lenght=16)
        self.property("ccName", type=str, required=True)
        self.property("extraLogo", type=Logo)


class TestCreditCardMetabuilder(TestCase):

    def setUp(self):
        self.cardBuilder = CreditCardMetaBuilder()

    def testa(self):
        self.cardBuilder.property("ccnumber", type=int, required=True, lenght=16)

    def testBuild(self):
        self.cardBuilder.ccnumber = "4304222233334444"
        self.cardBuilder.ccName = "Jhon Doe"
        self.cardBuilder.build()


