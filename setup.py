from setuptools import setup

setup(
    name='pipin',
    version='0.0.1',
    description='',
    author='Matt Lenc',
    author_email='matt.lenc@gmail.com',
    url='http://github.com/mattack108/pipin',
    license='LICENSE.txt',
    packages=['pipin'],
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'pipin = pipin:main',
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
