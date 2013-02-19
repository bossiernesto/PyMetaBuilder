__author__ = 'b03418'

import unittest
from PyMetaBuilder import MetaBuilder

class Person:
    pass

class PersonMetaBuilder(MetaBuilder.MetaBuilder):

    def __init__(self):
        self.model(Person)
        self.property('name')
        self.property('age',type=int)
        self.property('job',one_of=["doctor", "musician"])
        self.property('height',validates=self.myvalidator)
        self.required('name')

    def myvalidator(self,value):
        pass

class PyMetaBuilderTest(unittest.TestCase):

    def setUp(self):
        self.personMeta=PersonMetaBuilder()

    def test_hierarchy(self):
        self.assertIsInstance(self.personMeta,MetaBuilder.MetaBuilder)

    def test_should_able_to_add_model(self):
        self.assertEqual(Person,self.personMeta.getattr("_model"))

    def test_Attributes(self):
        self.assertTrue('name' in MetaBuilder.getAttributes(self.personMeta))
        self.assertTrue('age' in MetaBuilder.getAttributes(self.personMeta))
        self.assertTrue('job' in MetaBuilder.getAttributes(self.personMeta))
        self.assertTrue('height' in MetaBuilder.getAttributes(self.personMeta))

    def set_correctAttribute(self):
        self.personMeta.age=50


def test_something(self):
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
