import numpy as np


def failure():
    i = np.int(42)  # Noncompliant {{Replace this deprecated "numpy" type alias with the builtin type "int".}}
    #   ^^^^^^
    f = np.float(4.2)  # Noncompliant {{Replace this deprecated "numpy" type alias with the builtin type "float".}}
    #   ^^^^^^^^
    c = np.complex(-2.0, 0.0)  # Noncompliant {{Replace this deprecated "numpy" type alias with the builtin type "complex".}}
    #   ^^^^^^^^^^
    o = np.object  # Noncompliant {{Replace this deprecated "numpy" type alias with the builtin type "object".}}
    #   ^^^^^^^^^
    s = np.str("foo")  # Noncompliant {{Replace this deprecated "numpy" type alias with the builtin type "str".}}
    #   ^^^^^^
    l = np.long(123)  # Noncompliant {{Replace this deprecated "numpy" type alias with the builtin type "int".}}
    #   ^^^^^^^
    u = np.unicode("bar")  # Noncompliant {{Replace this deprecated "numpy" type alias with the builtin type "str".}}
    #   ^^^^^^^^^^

def failure_import_as_z():
    import numpy as z
    i = z.int(42)  # Noncompliant
    #   ^^^^^
    f = z.float(4.2)  # Noncompliant
    #   ^^^^^^^
    c = z.complex(-2.0, 0.0)  # Noncompliant
    #   ^^^^^^^^^
    o = z.object  # Noncompliant
    #   ^^^^^^^^
    s = z.str("foo")  # Noncompliant
    #   ^^^^^
    l = z.long(123)  # Noncompliant
    #   ^^^^^^
    u = z.unicode("bar")  # Noncompliant
    #   ^^^^^^^^^

def success():
    b = np.bool(True)
    b = np.bool(False)
    b = True  # Compliant
    b = bool(True)  # Compliant
    i = 42  # Compliant
    i = int(42)  # Compliant
    f = 4.2  # Compliant
    f = float(4.2)  # Compliant
    c = complex(-2.0, 0.0)  # Compliant
    o = object  # Compliant
    s = "foo"  # Compliant
    s = str("foo")  # Compliant
    l = 123  # Compliant
    l = int(123)  # Compliant
    u = "bar"  # Compliant
    u = str("bar")  # Compliant

def success_np_bool_usages():
    # np.bool is no longer deprecated (reintroduced in NumPy 2.x)
    arr = np.zeros(2).astype(np.bool)
    mask = np.ones((3, 4), dtype=np.bool)
    empty = np.zeros_like(arr, dtype=np.bool)
    if arr.dtype == np.bool:
        pass
    dtype = np.bool

