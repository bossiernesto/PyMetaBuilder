"""
.. module:: MetaBuilder Persona Test
   :platform: Linux
   :synopsis: An small framework for creating builders or entities with validators. Test Case for version >= 0.1.
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: GPL v3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>

"""
from unittest import TestCase
from PyMetabuilder import *


class Person(object):
    pass


class PersonMetaBuilder(MetaBuilder):

    def __init__(self):
        MetaBuilder.__init__(self)
        self.model(Person)
        self.property('name')
        self.property('age', type=int)
        self.property('job', one_of=["doctor", "musician"])
        self.property('height', validates=self.my_validator)
        self.required('name')

    def my_validator(self, value):
        return 1 < value <= 2.3


class PyMetaBuilderTest(TestCase):

    def setUp(self):
        self.personMeta = PersonMetaBuilder()

    def test_hierarchy(self):
        self.assertIsInstance(self.personMeta, MetaBuilder)

    def test_should_able_to_add_model(self):
        self.assertEqual(Person, self.personMeta.__getattribute__("_model"))

    def test_check_property_set(self):
        self.assertIn('validate_type_age', getMethods(self.personMeta))

    def test_get_validators_name(self):
        val = self.personMeta._getValidatorsByName('age')
        self.assertEqual('validate_type', val[0].__name__)

    def test_attributes(self):
        self.assertTrue('name' in self.personMeta.properties())
        self.assertTrue('age' in self.personMeta.properties())
        self.assertTrue('job' in self.personMeta.properties())
        self.assertTrue('height' in self.personMeta.properties())

    def test_correct_attribute_type(self):
        self.personMeta.age = 50
        self.assertEqual(50, self.personMeta.age)

    def test_incorrect_attribute_type(self):
        def setAge():
            self.personMeta.age = 'ssse'
        self.assertRaises(TypeError, setAge)

    def test_correct_attribute_options(self):
        self.personMeta.job = "doctor"
        self.assertEqual("doctor", self.personMeta.job)

    def test_incorrect_attribute_options(self):
        def setJob():
            self.personMeta.job = 'ssse'
        self.assertRaises(OptionValueError, setJob)

    def test_correct_custom_validator(self):
        self.personMeta.height = 2
        self.assertEqual(2, self.personMeta.height)

    def test_correct_custom_validator(self):
        def setMyHeight():
            self.personMeta.height = 22
        self.assertRaises(ValidatorError, setMyHeight)

    def test_required_not_filled(self):
        def build_without_required():
            self.personMeta.age = 20
            self.personMeta.build()
        self.assertRaises(AttributeError, build_without_required)

    def test_reserved_attribute(self):
        def reserved_word():
            self.personMeta.property("_model")
        self.assertRaises(MetaBuilderError, reserved_word)

    def test_build(self):
        self.personMeta.age = 50
        self.personMeta.name = 'John Doe'
        instance = self.personMeta.build()
        self.assertIsInstance(instance, Person)