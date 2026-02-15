=====================
ReturnValueWithStatus
=====================
The ``ReturnValueWithStatus`` class provides a data structure that allows you to
standardize the return value between classes and/or methods with the inclusion
of status and error information. Error information in the ``ReturnValueWithStatus``
instance should always be in de the for of an ``ErrorCode``.

Using the ReturnValueWithStatus instance allows you to unify the way the result status
of a return object is communicated throughout the chain of classes in your
project. Also the errors that were collected in lower level classes are
communicated throughout the chain of your classes. This is especially usefull
when you want a top level class to be able to report on errors that are created
in one or more of the lower level classes.

This setup was created with datapipelines in mind where the error can occur in
many different places in the pipeline and the pipeline might even return multiple errors.


Returning a ReturnValueWithStatus instance
------------------------------------------
Assume you have a method or a class that returns a data object. Evaluation of
the validaty of that data object should be done within that method. However the
result of that evevaluation needs to be propogated to the requesting method.

    from errors import ErrorCode, ReturnValueWithStatus

    result_is_none_error = ErrorCode(
	    code='GET_RESULT_0001',
	    description='Result is None')


	def get_result() -> ReturnValueWithStatus:
        """
        Method to retrieve a result object and return the result in a
        ReturnValueWithStatus instance.

        If retrieved result is None an error is added to the
        ReturnValueWithStatus object.
        """
        result_with_status = ReturnValueWithStatus(
            result=get_some_result())

        if result_with_status.result is None:
            result_with_status.add_error(result_is_none_error)

        return result_with_status


Validaty of ReturnValueWithStatus instance
------------------------------------------
``ReturnValueWithStatus`` instances contain a status via the is_valid property.
By default the status is ``True`` when no errors are attached to the instance.::

    >>> from errors import ReturnValueWithStatus
    >>> ReturnValueWithStatus().is_valid
    True

If an error is added the is_valid status will automatically change to ``False``.
::

    >>> from errors import ReturnValueWithStatus
    >>> return_value = ReturnValueWithStatus()
    >>> return_value.add_error(error)
    >>> return_value.is_valid
    False

If in some cases you would like the status not to be changed when you are adding
an error. You can do this by using the keep_current_status parameter when adding
the error. As the name suggest in this case the already existing status is kept.
::

    >>> from errors import ReturnValueWithStatus
    >>> return_value = ReturnValueWithStatus()
    >>> return_value.add_error(error1, keep_current_status=True)
    >>> return_value.is_valid
    True
    >>> return_value.add_error(error2)
    >>> return_value.is_valid
    False
    >>> return_value.add_error(error3, keep_current_status=True)
    >>> return_value.is_valid
    False


ReturnValueWithErrorStatus
--------------------------
When returning a ``ReturnValueWithStatus`` instance there will be situations
where you want to return default errors. These can be made with the
``ReturnValueWithStatus`` but you van make this process less verbose by using
the ``ReturnValueWithErrorStatus`` class.::

    from errors import ReturnValueWithErrorStatus, ReturnValueWithStatus

    class MyPipeline():
        def get_data(self):
            data = self.provide_data()
            if data is None:
                return ReturnValueWithErrorStatus(
                    error=error_code_result_is_none)

            return ReturnValueWithStatus(result=data)


``ReturnValueWithErrorStatus`` takes an error and returns a
``ReturnValueWithStatus`` with invalid status and provided error added to its
error list.


Typing the result attribute in ReturnValueWithStatus
----------------------------------------------------
The result attribute can have any type depening of course on what your data method is returning.
In order for this to work properly with the type checker you can define the type you expect from
the result attribute::

    from errors import ReturnValueWithStatus

    my_return_value = ReturnValueWithStatus[list[dict]]

    def data_from_pipeline(self):
        return my_return_value(result=data_method())

    # data_from_pipeline().result will be evaluated as type list[dict] by the type checker
