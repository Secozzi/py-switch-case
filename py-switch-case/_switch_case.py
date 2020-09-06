import re


class SwitchBaseException(Exception):
    """Base exception for Switch class"""
    pass


class InvalidCallException(SwitchBaseException):
    """Exception when a call is invalid"""
    pass


class UncallableFuncException(SwitchBaseException):
    """Exception when function is not callable"""
    pass


class InvalidRegexException(SwitchBaseException):
    """Exception when a regex match is invalid"""
    pass


class DuplicateKeyException(SwitchBaseException):
    """Exception when the two cases with the same key is listed twice or more"""
    pass


class NoDefaultException(SwitchBaseException):
    """Exception when a default case isn't provided"""
    pass


class CaseAfterDefaultException(SwitchBaseException):
    """Exception when a case is stated after the default"""
    pass


class NoResultException(SwitchBaseException):
    """Raised when result property is called when function stack hasn't returned anything"""
    pass


class Switch:
    """
    py-switch-case allows pytohn to utilize switch and case statements
    found in other languages.

    Usage:
    with switch(val) as s:
        s.case(4, do_stuff)
        s.call(lambda t: t < 5, do_other_stuff)
        s.match(reg1, reg2)
        s.default(default_stuff)

    s.result
    s.result_list
    """

    def __init__(self, switch_val, fallthrough=False):
        self._switch_val = switch_val
        self._fallthrough = fallthrough
        self._prev_fall = False
        self._used_default = False
        self._has_returned = False
        self._result = None
        self._used_keys = set()
        self._func_stack = []

        self._has_default = False

    def __enter__(self):
        return self

    def default(self, func):
        self._has_default = True
        if not self._func_stack:
            self._func_stack.append(func)

    def case(self, key, function, fallthrough=False):
        if self._has_default:
            raise CaseAfterDefaultException("Case after default is prohibited.")

        if key in self._used_keys:
            raise DuplicateKeyException(f"'{key}' is used in more than one case.")
        if not callable(function):
            raise UncallableFuncException(f"Function '{function}' is not callable.")

        self._used_keys.add(key)
        if key == self._switch_val:
            if self._prev_fall:
                self._func_stack.append(function)


            if self._func_stack:
                if fallthrough or self._fallthrough:
                    self._func_stack.append(function)
            else:
                self._func_stack.append(function)

        if fallthrough:
            self._prev_fall = True
        if self._fallthrough and not fallthrough:
            pass

    def __exit__(self, type, value, traceback):
        if value:
            raise value

        if not self._func_stack:
            raise NoDefaultException("No default case given or no matches.")

        if not self._has_default:
            raise NoDefaultException("No defult case given.")

        self._has_returned = True
        for func in self._func_stack:
            self._result = func()

    @property
    def result(self):
        if not self._has_returned:
            raise NoResultException("No result has been returned from any function.")
        else:
            return self._result


switch = Switch
