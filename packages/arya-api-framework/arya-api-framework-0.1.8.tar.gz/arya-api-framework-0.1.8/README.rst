Arya's API Framework
====================

.. list-table::
    :stub-columns: 1
    :widths: 10 90

    * - Docs
      - |docs|
    * - PyPI
      - |pypi-version| |supported-versions| |supported-implementations| |wheel|
    * - Activity
      - |commits-latest| |maintained| |pypi-downloads|
    * - QA
      - |codefactor|
    * - Other
      - |license| |language|

.. |docs| image:: https://img.shields.io/readthedocs/apiframework/latest?logo=read-the-docs&color=purple&logoColor=white
    :target: https://apiframework.readthedocs.io/en/latest/
    :alt: RTFD - Docs Build Status

.. |pypi-version| image:: https://img.shields.io/pypi/v/arya-api-framework?color=purple
    :target: https://pypi.org/project/arya-api-framework/
    :alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/arya-api-framework?logo=python&logoColor=white&color=purple
    :target: https://pypi.org/project/arya-api-framework/
    :alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/arya-api-framework?color=purple
    :target: https://pypi.org/project/arya-api-framework/
    :alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/arya-api-framework?color=purple
    :target: https://pypi.org/project/arya-api-framework/
    :alt: PyPI - Wheel

.. |commits-latest| image:: https://img.shields.io/github/last-commit/Aryathel/ApiFramework/main?color=purple
    :target: https://github.com/Aryathel/APIFramework
    :alt: Github - Last Commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2022?color=purple
    :target: https://github.com/Aryathel/APIFramework/commit/main
    :alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/arya-api-framework?color=purple
    :target: https://pypistats.org/packages/arya-api-framework
    :alt: PyPI - Downloads

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/Aryathel/ApiFramework?logo=codefactor&color=purple&logoColor=white
    :target: https://www.codefactor.io/repository/github/Aryathel/ApiFramework
    :alt: CodeFactor - Grade

.. |license| image:: https://img.shields.io/github/license/Aryathel/ApiFramework?color=purple
    :target: https://github.com/Aryathel/ApiFramework/blob/main/LICENSE
    :alt: GitHub - License

.. |language| image:: https://img.shields.io/github/languages/top/Aryathel/ApiFramework?color=purple
    :target: https://github.com/Aryathel/ApiFramework
    :alt: GitHub - Top Language

This is a simple package that is meant to be a
`Pydantic <https://pydantic-docs.helpmanual.io/>`__ implementation
for a basic RESTful API interaction client. This includes both sync and async usages.

Installation
------------
Synchronous implementation - if you aren't sure, you probably want this:

.. code-block:: sh

    python -m pip install arya-api-framework[sync]

Asynchronous implementation:

.. code-block:: sh

    python -m pip install arya-api-framework[async]

Documentation
-------------

https://apiframework.readthedocs.io/en/latest/

TODO Features
-------------

- [ ] Response caching.

Citation
--------
Credit for documentation infrastructure goes to `Rapptz <https://github.com/Rapptz>`_ and the
`discord.py <https://github.com/Rapptz/discord.py>`_ team. The documentation for this project is a modified version of
their custom theme.