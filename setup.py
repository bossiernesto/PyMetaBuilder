from distutils.core import setup

with open('README.rst') as readme:
    long_description = readme.read()

setup(name="PyMetaBuilder",
      version="0.2.0",
      description="Small framework for creating Builders and entities",
      long_description=long_description,
      author="Ernesto Bossi",
      author_email="bossi.ernestog@gmail.com",
      url="https://github.com/bossiernesto/PyMetaBuilder",
      license="GPL v3",
      py_modules=["PyMetaBuilder"],
      keywords="MetaBuilder Metaprogramming",
      classifiers=["Development Status :: 3 - Alpha",
                   "Topic :: Utilities",
                   "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"]
)

