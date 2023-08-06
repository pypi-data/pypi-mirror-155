from setuptools import setup, Extension

digibyte_scrypt_module = Extension('digibyte_scrypt',
                               sources = ['digibyte_scrypt/scryptmodule.c',
                                          'digibyte_scrypt/scrypt.c'],
                               include_dirs=['./digibyte_scrypt/'])

long_description = open("README.md", "r").read()

setup (
    maintainer = 'YoshiJaeger',
    maintainer_email = 'pypi@jaeger.berlin',
    url = 'https://pypi.org/project/digibyte_scrypt',
    name = 'digibyte_scrypt',
    version = '1.0.3',
    description = 'Bindings for scrypt proof of work used by DigiByte',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = 'GPLv3',
    include_package_data = True,
    classifiers = [
        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.10',
    ],
    ext_modules = [digibyte_scrypt_module],
)
