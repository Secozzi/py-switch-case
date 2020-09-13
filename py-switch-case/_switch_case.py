import re


class SwitchBaseException(Exception):
    """Base exception for Switch class"""
    pass


class NotImplementedException(SwitchBaseException):
    """Exception when a case is matched with an unimplemented type"""
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
    py-switch-case allows python to utilize switch and case statements
    found in other languages. Note: refrain from using anything besides
    strings, float, and integers as value unless absolutely necessary.

    Usage:
    with switch(val) as s:
        s.case(4, do_stuff)
        s.call(lambda t: t < 5, do_other_stuff)
        s.match(reg1, do_third_stuff)
        s.default(default_stuff)

    print(s.result)
    """

    def __init__(self, switch_val):
        self._switch_val = switch_val
        self._used_default = False
        self._found_match = False
        self._result = None
        self._used_keys = []
        self._func_stack = []

        self._has_returned = False
        self._has_default = False

    def __enter__(self):
        return self

    def default(self, func):
        self._has_default = True
        if not self._found_match:
            self._func_stack.append(func)

    def case(self, key, function):
        """
        Define a case.

        Cases can be called with either:
            * String, Integer, or Float - This will try to match with ==
            * List or Range - This will use Python's 'in' keyword
            * Anything else and it will throw an error

        :param key: str, int, float, list, or range
            Key to match switch statement with
        :param function: Function
            Function to call if matched
        :return:
            Doesn't return
        """
        if self._has_default:
            raise CaseAfterDefaultException("Case after default is prohibited.")

        if key in self._used_keys:
            raise DuplicateKeyException(f"'{key}' is used in more than one case.")

        if not callable(function):
            raise UncallableFuncException(f"Function '{function}' is not callable.")

        self._used_keys.append(key)
        if not self._found_match:
            if isinstance(key, str) or isinstance(key, int) or isinstance(key, float):
                if self._switch_val == key:
                    self._func_stack.append(function)
                    self._found_match = True

            elif isinstance(key, list) or isinstance(key, range):
                if self._switch_val in key:
                    self._func_stack.append(function)
                    self._found_match = True

            else:
                raise NotImplementedException(f"Case with type '{type(key)} is not yet supported'")

    def match(self, regex, function, convert=True, compilation_flag=None):
        """
        Match against a regular expression.

        :param regex: str
            String representation of regular expression
        :param function: Function
            Function to call if match
        :param convert: Bool
            Convert switch value to string. Set to false to not convert. True by default
        :param compilation_flag: str
            Regex flags
        :return:
            Doesn't return
        """
        if compilation_flag:
            _reg = re.compile(regex, compilation_flag)
        else:
            _reg = re.compile(regex)

        if _reg in self._used_keys:
            raise DuplicateKeyException(f"Regular expression '{_reg}' is used in more than one case.")

        self._used_keys.append(_reg)
        if not self._found_match:
            if convert:
                _to_match = str(self._switch_val)
            else:
                _to_match = self._switch_val

            if not isinstance(_to_match, str):
                raise InvalidRegexException(f"Cannot use regex on {type(_to_match)}")

            _match = _reg.match(_to_match)

            if _match:
                self._func_stack.append(function)
                self._found_match = True

    def call(self, callable_func, function):
        """
        Callable match.

        :param callable_func: Function
            Function to match against. Must contain one and only one argument
        :param function: Function
            Function to call if match
        :return:
            Doesn't return
        """
        if callable_func in self._used_keys:
            raise DuplicateKeyException(f"Function '{callable_func}' is used in more than one case.")

        self._used_keys.append(callable_func)
        if not self._found_match:
            if not callable(callable_func):
                raise UncallableFuncException(f"{callable_func} is not callable")

            _result = callable_func(self._switch_val)

            if _result:
                self._func_stack.append(function)
                self._found_match = True

    def __exit__(self, type, value, traceback):
        if value:
            raise value

        if not self._func_stack:
            raise NoDefaultException("No default case given or no matches.")

        if not self._has_default:
            raise NoDefaultException("No defult case given.")

        for func in self._func_stack:
            self._result = func()
        if self._result:
            self._has_returned = True

    @property
    def result(self):
        if not self._has_returned:
            raise NoResultException("No result has been returned from any function.")
        else:
            return self._result


switch = Switch
