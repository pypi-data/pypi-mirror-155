from setuptools import setup
import pathlib
import re

# Build with: python -m build && python -m twine upload --repository pypi dist/*

project = None
with open('arya_api_framework/__init__.py') as f:
    project = re.search(r'^__project__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)
    if not project:
        raise RuntimeError('__project__ is not set.')
copyright = None
with open('arya_api_framework/__init__.py') as f:
    copyright = re.search(r'^__copyright__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)
    if not copyright:
        raise RuntimeError('__copyright__ is not set.')
author = None
with open('arya_api_framework/__init__.py') as f:
    author = re.search(r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)
    if not author:
        raise RuntimeError('__author__ is not set.')
version = None
with open('arya_api_framework/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)
    if not version:
        raise RuntimeError('__version__ is not set.')
title = None
with open('arya_api_framework/__init__.py') as f:
    title = re.search(r'^__title__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)
    if not title:
        raise RuntimeError('__title__ is not set.')
license_type = None
with open('arya_api_framework/__init__.py') as f:
    license_type = re.search(r'^__license__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)
    if not title:
        raise RuntimeError('__license__ is not set.')

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.rst").read_text(encoding="utf-8")

requirements = [
    "pydantic>=1.9.1",
    "yarl>=1.7.2"
]

extras_require = {
    "sync": ["requests>=2.27.1", "ratelimit>=2.2.1"],
    "async": ["aiohttp>=3.8.1", "aiolimiter>=1.0.0"]
}

packages = [
    "arya_api_framework",
    "arya_api_framework.async_framework",
    "arya_api_framework.sync_framework",
]

setup(
    name=title,
    version=version,
    description="A simple API framework used in many other API clients I create.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Aryathel/ApiFramework",
    project_urls={'Documentation': 'https://apiframework.readthedocs.io/en/latest/'},
    author="Aryathel",
    license=license_type,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10.0",
    packages=packages,
    install_requires=requirements,
    extras_require=extras_require,
    include_package_data=True
)
