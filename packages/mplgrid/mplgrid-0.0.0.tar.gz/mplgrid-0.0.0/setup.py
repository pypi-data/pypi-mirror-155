""" Setup for installing mplgrid."""

from setuptools import setup

__version__ = "0.0.0"

with open('README.md', encoding='utf-8') as readme_file:
    README = readme_file.read()

INSTALL_REQUIRES = ['matplotlib',
                    'numpy',
                    ]

# Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'Intended Audience :: Science/Research',
               'License :: OSI Approved :: MIT License',
               'Operating System :: OS Independent',
               'Framework :: Matplotlib',
               'Programming Language :: Python :: 3 :: Only',
               'Topic :: Scientific/Engineering :: Visualization']

setup(name='mplgrid',
      version=__version__,
      description='A Python package for creating a grid of axes in Matplotlib.',
      long_description_content_type="text/markdown",
      long_description=README,
      classifiers=CLASSIFIERS,
      url='https://github.com/andrewRowlinson/mplgrid',
      author='Andrew Rowlinson',
      author_email='rowlinsonandy@gmail.com',
      author_twitter='@numberstorm',
      license='MIT',
      packages=['mplgrid'],
      python_requires='>=3.6',
      install_requires=INSTALL_REQUIRES,
      setup_requires=INSTALL_REQUIRES,
      zip_safe=False)
