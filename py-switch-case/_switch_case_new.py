# Trying out new
import sys


class SkipWithBlock(Exception):
    pass


class Case:
    def __init__(self, value, key):
        self._value = value
        self._key = key

    def __enter__(self):
        if self._value != self._key:
            sys.settrace(lambda *args, **keys: None)
            frame = sys._getframe(1)
            frame.f_trace = self.trace

    def trace(self, frame, event, arg):
        raise SkipWithBlock()

    def __exit__(self, type, value, traceback):
        if type is None:
            return
        if issubclass(type, SkipWithBlock):
            return True


class Switch:
    def __init__(self, switch_val):
        self._switch_val = switch_val
        self._case = Case

    def __enter__(self):
        return self

    def case(self, key):
        return self._case(self._switch_val, key)

    def __exit__(self, type, value, traceback):
        pass


val = 7
with Switch(val) as s:
    with s.case(7):
        print("Matched 7!")
    with s.case(4):
        print("Matched 4!")