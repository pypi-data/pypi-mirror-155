#!/usr/bin/env python3

"""
** Configuration file for pypi. **
----------------------------------
"""

import setuptools

import deformation

with open('README.rst', 'r', encoding='utf-8') as file:
    long_description = file.read()

setuptools.setup(
    name='deformation',
    version=deformation.__version__,
    author='Robin RICHARD (robinechuca)',
    author_email='serveurpython.oz@gmail.com',
    description='Chain image distortion.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://framagit.org/robinechuca/deformation/-/blob/main/README.rst',
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'opencv-python', 'sympy', 'torch'],
    extras_require={
        'dev': ['pytest', 'pylint', 'pdoc3', 'pyreverse', 'context-verbose', 'matplotlib'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
    keywords=[
        'image',
        'dewarping',
        'warping'
        'warp',
        'deformation',
        'distortion',
    ],
    python_requires='>=3.6',
    project_urls={
        'Source Repository': 'https://framagit.org/robinechuca/deformation',
        'Documentation': 'http://python-docs.ddns.net/deformation/',
    },
    include_package_data=True,
)
