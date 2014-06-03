from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

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
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='pipin',
    version='0.2.2',
    author='Maciek Lenc',
    author_email='matt.lenc@gmail.com',
    url='http://github.com/mattack108/pipin',
    license='MIT',
    description='pipin is a little script to search for dependencies within'
                'your project(s).',
    install_requires=install_requires,
    cmdclass={'test': PyTest},
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pipin = pipin:run',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='pipin pip requirements dependencies',
)
