from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Enarksh',

    version='0.9.0',

    description='A lightweight and powerful job scheduler',
    long_description=long_description,

    url='https://github.com/SetBased/py-enarksh',

    author='Set Based IT Consultancy',
    author_email='info@setbased.nl',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Code Generators',
        'Topic :: System :: Installation/Setup',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='job, scheduler',

    packages=find_packages(exclude=['build', 'test']),

    install_requires=['cleo==0.5.0', 'pystratum-mysql', 'pyzmq', 'lxml', 'python-daemon'],

    entry_points={}
)
