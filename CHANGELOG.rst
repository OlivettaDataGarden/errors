
Changelog
=========

1.4.4 (2024-05-23)
------------------
* Added typevar for ReturnValueWithStatus result attribute

1.4.0 (2024-05-23)
------------------
* Added ``ErrorListByMixin`` class to support autocompletion and type checking of your custom project errors

1.3.2 (2023-10-23)
------------------
* Added support for python 3.12

1.3.1 (2023-10-20)
------------------
* Refactored setup.cfg and pyproject.toml

1.3.0 (2022-11-01)
------------------
* Added type annotations

1.2.4 (2022-10-26)
------------------
* Added support for python 3.11

1.2.2 (2022-05-09)
------------------
* Added ``ReturnValueWithErrorStatus`` to __init__ for easy import.

1.2.1 (2022-05-08)
------------------
* Added a class ``ReturnValueWithErrorStatus`` to easily create
  ``ReturnValueWithStatus`` with a error attached to it.

1.2.0 (2022-05-06)
------------------
* Added a dataclass ``ReturnValueWithStatus`` to allow consuming classes and
  methods to return a single return type with result, status and errors
  collected in one Object

1.1.1 (2021-11-06)
------------------
* Import ``ListErrors``, ``ErrorCode``, ``add_error_data()`` and ``is_error()``
  in ``errors`` ``__init__.py`` so that they can be directly imported from ``errors`` module

1.1.0 (2021-11-05)
------------------
* Added is_error method to check if an object is an instance of
  (sub)class ``ErrorCode``

1.0.0 (2021-10-12)
------------------
* Added Documentation and removed more default but redundant Documentation
* Added reference documentation for ``ListErrors`` and ``base`` module

0.9.0 (2021-10-11)
------------------
* added error codes as attribut to ListErrors class.
  After registration of an ErrorCode the errorcode is accessible in
  ``ListErrors`` via::

      ListErrors.ERROR_CODE_KEY

* Added Documentation and removed default redundant Documentation

0.1.0 (2021-10-08)
------------------
* First release on PyPI.
