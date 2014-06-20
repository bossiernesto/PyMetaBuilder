import unittest
from PyMetabuilder.MetaBuilder import MetaBuilder, OptionValueError

class TestMetaBuilder(unittest.TestCase):
    def setUp(self):
        self.kite_builder = MetaBuilder()

        #create a kite
        self.kite_builder.model_by_name('Kite')\
            .property('string_material', one_of=["linen", "normal_string"])\
            .property('kite_shape', required=True)

    def test_kite_bad_setup(self):
        self.kite_builder.kite_shape = 'an strange material'
        self.assertRaises(OptionValueError, self.kite_builder.string_material, 'cotton')

    def test_kite_good_setup(self):
        kite_shape = 'an strange material'
        self.kite_builder.kite_shape = kite_shape
        string_material = 'linen'
        self.kite_builder.string_material = string_material
        kite = self.kite_builder.build()
        self.assertEqual(string_material,kite.string_material)
        self.assertEqual(kite_shape,kite.kite_shape)