import unittest
from PyMetaBuilder.property import PropertyBuilder,rebind
from PyMetaBuilder.MetaBuilder import getMethodsByName
import inspect

class A:

    def dosome(self):
        print 333

class testDynamicProperty(unittest.TestCase):

    def setUp(self):
        self.a = A()

    def testBuildProperty(self):
        class C:
            pass
        c=C()
        p=PropertyBuilder()
        print dir(self.a)
        p.buildProperty(self.a,'saraza',2)
        self.assertEqual(self.a.saraza,2)
        p.buildProperty(c,'j',2)
        self.assertEqual(c.j,2)

    def testBuildPropertiesString(self):
        PropertyBuilder().buildProperty(self.a,'dato',"ddd")
        self.assertEqual(self.a.dato,"ddd")

    def testBuildProperties(self):
        PropertyBuilder().buildProperties(self.a,{'dato':"ddd","saraza":2})
        self.assertEqual(self.a.dato,"ddd")
        self.assertEqual(self.a.saraza,2)
        self.a.saraza=4

    def testAssignInstance(self):
        class B:
            pass
        b=B()
        PropertyBuilder().buildProperty(self.a,'instanceB',b)
        self.assertEqual(b,self.a.instanceB)

    def testCode(self):
        prop=PropertyBuilder()
        PropertyBuilder().migrateMethods(self.a)
        rebind(prop.getPrivateMehtods,self.a)
        for methodProp,methodA in (zip(prop.getPrivateMehtods(),self.a.getPrivateMehtods())):
            self.assertEqual(inspect.getsource(methodProp),inspect.getsource(methodA))
