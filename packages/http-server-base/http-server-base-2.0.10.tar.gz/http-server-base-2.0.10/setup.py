# noinspection PyProtectedMember
from setuptools import _install_setup_requires
_install_setup_requires(dict(setup_requires=[ 'extended-setup-tools' ]))

from extended_setup import ExtendedSetupManager
ExtendedSetupManager('http_server_base').setup \
(
    short_description = "Python implementation of Scala-like monadic data types.",
    license = "MIT Licence",
    description = "Library for simple HTTP server & REST HTTP server base based on Tornado. Includes: Logging requests and responses with Request Id; Configuration loading; Methods for requests proxying",
    min_python_version = '3.6.0',
    keywords = [ 'http', 'tornado', 'server', 'http-server', 'restapi', 'rest' ],
    classifiers =
    [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: Proxy Servers',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ]
)
