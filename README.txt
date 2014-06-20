PyMetaBuilder
=============

Introduction
------------

Small framework to create entities and Builders with Metaprogramming
features in Python.

Creating Builders
-----------------

Metabuilder objective is to help to create Builders and instances or
entities with validations easy and fast.

In order to create a new Builder just define a class extending from
MetaBuilder class, and defining an stub class in any place you want. For
eg.

::

    from PyMetaBuilder import MetaBuilder

    #Stub Class to create instances from
    class Kite(object):
        pass

    class KiteBuilder(MetaBuilder):
        pass

.. note:: from version 0.2.1 onwards you can define the class model with the method model_by_name, thus you don't have to define a stub class in your code. For ex. calling model_by_name('Kite') instead of model(Kite)

After that just initiate the superclass and start defining the
properties you want KiteBuilder to have, for eg.

::

    class KiteBuilder(MetaBuilder):

        def __init__(self):
            MetaBuilder.MetaBuilder.__init__(self)
            self.defineKite()

        def define_kite(self):
            #define the model klass to get instances from
            self.model(Kite)
            self.property("design",one_of=["Indoor","Water Kite","Kythoon"])
            self.property("line_material",type=str)
            self.property("StringLength",type=int)

You can also define a property as a mandatory one, with the required
method. In this way, when you set the builder with the respecting
properties and try to get a new instance, the framework will check if
the properties that you previously set as mandatory were set.

::

           def define_kite(self):
            #define the model klass to get instances from
            self.model(Kite)
            self.property("StringLength",type=int)
            #code defining properties....
            self.required("design")

Creating instances from a Builder
---------------------------------

After you defined a builder and its properties, just set the parameters,
if you want at this time and if they're not mandatory and build an
instance.

::

           kiteBuilder=KiteBuilder()
           kiteBuilder.design="Indoor"
           kiteBuilder.StringLength=23

           kite=kiteBuilder.build() #get a Kite instance

When you set a property that you previously defined, it'll validate the
value passed, given the fact that you have set it with validators, and
will generate the appropriate exception when it fails.