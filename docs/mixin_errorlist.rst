=================
 ErrorListByMixin
=================


Define your errors list using ``ErrorListByMixin``
--------------------------------------------------

When using the register method on the ``ListErrors`` class you will face issues with static type
checkers and autocompletion. Static type checker and autocompletion will not evaluate the
registrations of error codes as these are done only in run time.

The class ``ErrorListByMixin`` provides an alteranative way to create a single class with all
errorcodes. ``This ErrorListByMixin`` class has the advantage that type checkers and
autocompletion will recognize all your error codes. The disadvantage is that you need
to mixin all definitions of your errorcodes in a central custom class with the
``ErrorListByMixin`` class::

    from errors import ErrorListByMixin
    from your_local_module1 import ModOneErrorcodes
    from your_local_module2 import ModTwoErrorcodes

    class MyProjectErrorCodes(ErrorListByMixin, ModOneErrorcodes, ModTwoErrorcodes): ...

    MyProjectErrorCodes.ERROR_FROM_MOD_ONE    # this now does not create type checking issues
