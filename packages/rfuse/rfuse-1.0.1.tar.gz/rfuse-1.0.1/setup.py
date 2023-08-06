import pathlib

from setuptools import setup, find_packages

"""
Setup module for Fuse
"""

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name='rfuse',
    description='Fuse is a content aggregation CLI tool written in Python',
    long_description=README,
    long_description_content_type="text/markdown",
    version='1.0.1',
    license='MIT',
    author="Eliran Turgeman",
    author_email='email@example.com',
    python_requires=">=3.7",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Eliran-Turgeman/Fuse',
    keywords='Fuse aggregation',
    install_requires=[
        'feedparser==6.0.8',
        'praw==6.4.0',
        'colorama==0.4.4',
        'pytest',
        'pytest-mock==3.7.0',
        'requests'
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
