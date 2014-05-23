import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

import pipin

install_requires = []
if sys.version_info[:2] < (2, 7):
    install_requires.append('argparse')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='pipin',
    version=pipin.__version__,
    description='',
    author='Matt Lenc',
    author_email='matt.lenc@gmail.com',
    url='http://github.com/mattack108/pipin',
    license='LICENSE.txt',
    packages=['pipin'],
    install_requires=install_requires,
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    test_suite='pipin.tests.test_pipin',
    extras_require={
        'testing': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'pipin = pipin.pipin:lets_pipin',
        ]
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ]
)
