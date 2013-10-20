import unittest
from PyMetabuilder.MetaBuilder import MetaBuilder


class TestearMetaBuilder(unittest.TestCase):
    def setUp(self):
        self.kite_builder = MetaBuilder()

        #create a kite
        self.kite_builder.model_by_name('Kite')
        self.kite_builder.property('string_material', one_of=["linen", "normal_string"])
        self.kite_builder.property('kite_shape', required=True)

        self.kite = self.kite_builder.build()

    def test_kite_bad_setup(self):
        self.kite_builder.kite_shape='an strange material'
        self.kite_builder.string_material='cotton'
        self.kite_builder.build()