from distutils.core import setup

with open('README.txt') as readme:
    long_description = readme.read()

setup(name="PyMetabuilder",
      version="0.2.4",
      description="Small framework for creating Builders and entities",
      long_description=long_description,
      author="Ernesto Bossi",
      author_email="bossi.ernestog@gmail.com",
      url="https://github.com/bossiernesto/PyMetabuilder",
      license="GPL v3",
      packages=['PyMetabuilder'],
      package_dir={'PyMetabuilder': 'PyMetabuilder'},
      keywords="MetaBuilder Metaprogramming",
      classifiers=["Development Status :: 4 - Beta",
                   "Topic :: Utilities",
                   "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"]
)

