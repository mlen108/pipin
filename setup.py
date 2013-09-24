import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

import pipin


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
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ]
)
