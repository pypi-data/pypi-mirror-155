from setuptools import setup, find_packages

classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()


setup(
    name                 = 'simplereq',
    version              = '0.5.0',
    description          = 'A simple python library that is similar to requests.',
    long_description = long_description,
    author               = 'Jiro',
    author_email         = 'contact@jiroawesome.tech',
    url                  = '',
    py_modules           = ['simplereq'],
    license              = 'MIT',
    include_package_data = True
    )