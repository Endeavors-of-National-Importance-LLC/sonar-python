
def property(func):
    """A user-defined decorator that happens to be named 'property'."""
    return func


class UserDefinedPropertyDecorator:
    def __init__(self):
        self._value = 0

    @property
    def value(self):  # Compliant - built-in 'property' is shadowed by the user-defined decorator above; type matcher correctly excludes this
        self._value * 2

