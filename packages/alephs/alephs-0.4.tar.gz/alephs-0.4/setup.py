#!/usr/bin/env python


from setuptools import setup, find_packages

setup(
    name='alephs',
    py_modules=None,
    version="0.4",
    keywords=["Pakistani", "emergency", "services", "internet"],
    description="(A) (L)ist of (E)mergency (P)akistani (H)elp (S)ervices.",
    long_description=open('README.md').read(),

    project_urls={
        'Homepage': 'https://www.techtum.dev/work-alephs-220621.html',
        'Source': 'https://github.com/siphr/alephs',
        'Tracker': 'https://github.com/siphr/alephs/issues',
    },
    author="siphr",
    author_email="pypi@techtum.dev",

    packages=['alephs'],
    package_data = {
        'alephpk':['data/institutions.json']
        },
    platforms="any",
)
