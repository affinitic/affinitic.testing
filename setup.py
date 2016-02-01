from setuptools import setup, find_packages
import os

version = '0.1.11'

setup(
    name='affinitic.testing',
    version=version,
    description="Test tools",
    long_description=open(os.path.join("docs", "HISTORY.rst")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Test tools',
    author='Affinitic',
    author_email='info@affinitic.be',
    url='http://github.com/affinitic/affinitic.testing/',
    license='gpl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['affinitic'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'affinitic.db',
        'mock',
        'setuptools',
        'sqlparse',
        'unittest2',
        'zope.component',
    ],
    extras_require=dict(
        test=['plone.testing']),
    entry_points="""
    # -*- Entry points: -*-
    """,
)
