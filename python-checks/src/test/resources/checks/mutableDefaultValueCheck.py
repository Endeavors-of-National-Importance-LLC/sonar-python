def noncompliant_examples():
    """Examples that should trigger the rule."""

    # Section: dict.fromkeys with list literal
    def dict_fromkeys_list_literal():
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, [])  # Noncompliant {{Replace this mutable value with an immutable default to avoid shared state.}}
        #                             ^^

    def dict_fromkeys_dict_literal():
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, {})  # Noncompliant {{Replace this mutable value with an immutable default to avoid shared state.}}
        #                             ^^

    def dict_fromkeys_set_literal():
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, {1, 2, 3})  # Noncompliant {{Replace this mutable value with an immutable default to avoid shared state.}}
        #                             ^^^^^^^^^

    def dict_fromkeys_list_constructor():
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, list())  # Noncompliant {{Replace this mutable value with an immutable default to avoid shared state.}}
        #                             ^^^^^^

    def dict_fromkeys_dict_constructor():
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, dict())  # Noncompliant
        #                             ^^^^^^

    def dict_fromkeys_set_constructor():
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, set())  # Noncompliant
        #                             ^^^^^

    def dict_fromkeys_bytearray_constructor():
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, bytearray())  # Noncompliant
        #                             ^^^^^^^^^^^

    def dict_fromkeys_list_with_elements():
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, [1, 2, 3])  # Noncompliant
        #                             ^^^^^^^^^

    def dict_fromkeys_dict_with_elements():
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, {'x': 1})  # Noncompliant
        #                             ^^^^^^^^

    def dict_fromkeys_from_import():
        from builtins import dict as d
        keys = range(5)
        my_dict = d.fromkeys(keys, [])  # Noncompliant
        #                          ^^

    # Section: ContextVar with mutable defaults
    def contextvar_list_literal():
        from contextvars import ContextVar
        my_var = ContextVar('my_var', default=[])  # Noncompliant
        #                                     ^^

    def contextvar_dict_literal():
        from contextvars import ContextVar
        my_var = ContextVar('my_var', default={})  # Noncompliant
        #                                     ^^

    def contextvar_set_literal():
        from contextvars import ContextVar
        my_var = ContextVar('counter', default={1, 2})  # Noncompliant
        #                                      ^^^^^^

    def contextvar_list_constructor():
        from contextvars import ContextVar
        my_var = ContextVar('my_var', default=list())  # Noncompliant
        #                                     ^^^^^^

    def contextvar_dict_constructor():
        from contextvars import ContextVar
        my_var = ContextVar('my_var', default=dict())  # Noncompliant
        #                                     ^^^^^^

    def contextvar_set_constructor():
        from contextvars import ContextVar
        my_var = ContextVar('my_var', default=set())  # Noncompliant
        #                                     ^^^^^

    def contextvar_bytearray_constructor():
        from contextvars import ContextVar
        my_var = ContextVar('buffer', default=bytearray())  # Noncompliant
        #                                     ^^^^^^^^^^^

    def contextvar_list_with_elements():
        from contextvars import ContextVar
        my_var = ContextVar('items', default=[1, 2, 3])  # Noncompliant
        #                                    ^^^^^^^^^

    def contextvar_fully_qualified():
        import contextvars
        my_var = contextvars.ContextVar('my_var', default=[])  # Noncompliant
        #                                                 ^^

    def dict_fromkeys_bytearray_with_args():
        keys = ['x', 'y']
        my_dict = dict.fromkeys(keys, bytearray(b'abc'))  # Noncompliant
        #                             ^^^^^^^^^^^^^^^^^

    # Section: Variable propagation via reaching definitions analysis
    def dict_fromkeys_variable_default():
        keys = ['a', 'b', 'c']
        default_value = []
        my_dict = dict.fromkeys(keys, default_value)  # Noncompliant
        #                             ^^^^^^^^^^^^^

    def contextvar_variable_default():
        from contextvars import ContextVar
        initial = []
        my_var = ContextVar('my_var', default=initial)  # Noncompliant
        #                                     ^^^^^^^

    def dict_fromkeys_variable_dict_literal():
        keys = ['a', 'b', 'c']
        default_value = {}
        my_dict = dict.fromkeys(keys, default_value)  # Noncompliant
        #                             ^^^^^^^^^^^^^

    def dict_fromkeys_variable_set_literal():
        keys = ['a', 'b', 'c']
        default_value = {1, 2}
        my_dict = dict.fromkeys(keys, default_value)  # Noncompliant
        #                             ^^^^^^^^^^^^^

    def dict_fromkeys_variable_list_constructor():
        keys = ['a', 'b', 'c']
        default_value = list()
        my_dict = dict.fromkeys(keys, default_value)  # Noncompliant
        #                             ^^^^^^^^^^^^^

    def contextvar_variable_dict_constructor():
        from contextvars import ContextVar
        initial = dict()
        my_var = ContextVar('my_var', default=initial)  # Noncompliant
        #                                     ^^^^^^^

    # Section: Conditional assignment where all branches are mutable
    def dict_fromkeys_conditional_all_mutable():
        keys = ['a', 'b', 'c']
        if some_condition:
            default_value = []
        else:
            default_value = {}
        my_dict = dict.fromkeys(keys, default_value)  # Noncompliant
        #                             ^^^^^^^^^^^^^

    def contextvar_conditional_all_mutable():
        from contextvars import ContextVar
        if some_condition:
            initial = set()
        else:
            initial = []
        my_var = ContextVar('my_var', default=initial)  # Noncompliant
        #                                     ^^^^^^^


def compliant_examples():
    """Examples that should NOT trigger the rule."""

    def dict_fromkeys_no_default():
        # No second argument — no shared mutable default
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys)

    def dict_fromkeys_none_default():
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, None)

    def dict_fromkeys_string_default():
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, "default")

    def dict_fromkeys_int_default():
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, 0)

    def dict_fromkeys_tuple_default():
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, (1, 2, 3))

    def dict_fromkeys_frozenset_default():
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, frozenset({1, 2, 3}))

    def dict_fromkeys_function_return_default():
        # Cannot determine what compute_default() returns statically
        def compute_default():
            return []
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, compute_default())

    def contextvar_no_default():
        from contextvars import ContextVar
        my_var = ContextVar('my_var')

    def contextvar_none_default():
        from contextvars import ContextVar
        my_var = ContextVar('my_var', default=None)

    def contextvar_string_default():
        from contextvars import ContextVar
        my_var = ContextVar('my_var', default="initial")

    def contextvar_int_default():
        from contextvars import ContextVar
        my_var = ContextVar('counter', default=0)

    def contextvar_tuple_default():
        from contextvars import ContextVar
        my_var = ContextVar('my_var', default=(1, 2, 3))

    def contextvar_frozenset_default():
        from contextvars import ContextVar
        my_var = ContextVar('my_var', default=frozenset({1, 2}))

    def contextvar_function_return_default():
        from contextvars import ContextVar
        def make_default():
            return []
        my_var = ContextVar('my_var', default=make_default())

    def dict_fromkeys_conditional_one_immutable():
        # At least one branch assigns an immutable value — do not raise
        keys = ['a', 'b', 'c']
        if some_condition:
            default_value = []
        else:
            default_value = None
        my_dict = dict.fromkeys(keys, default_value)

    def contextvar_conditional_one_immutable():
        from contextvars import ContextVar
        if some_condition:
            initial = "safe"
        else:
            initial = []
        my_var = ContextVar('my_var', default=initial)

    def dict_fromkeys_variable_immutable():
        keys = ['a', 'b', 'c']
        default_value = 0
        my_dict = dict.fromkeys(keys, default_value)

    def contextvar_variable_immutable():
        from contextvars import ContextVar
        initial = "hello"
        my_var = ContextVar('my_var', default=initial)

    def dict_fromkeys_variable_from_function():
        # Function return — reaching definitions won't resolve this
        keys = ['a', 'b', 'c']
        default_value = some_function()
        my_dict = dict.fromkeys(keys, default_value)

    def not_dict_fromkeys():
        # A different class with a fromkeys method — not builtins.dict
        class MyMapping:
            @classmethod
            def fromkeys(cls, keys, value=None):
                return {}
        my_dict = MyMapping.fromkeys(['a', 'b'], [])

    def not_context_var():
        # A class also named ContextVar but not from contextvars
        class ContextVar:
            def __init__(self, name, default=None):
                pass
        my_var = ContextVar('my_var', default=[])


def edge_cases():
    """Corner cases and static analysis limitations."""

    def dict_fromkeys_keyword_second_arg():
        # Second arg passed as keyword — not checked (only positional at index 1 is inspected)
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, value=[])

    def dict_fromkeys_starred_args():
        # Unpacked positional args — static analysis cannot inspect the value
        keys = ['a', 'b', 'c']
        args = (keys, [])
        my_dict = dict.fromkeys(*args)

    def contextvar_positional_default():
        # Default passed positionally rather than by keyword — not flagged
        # because the check only inspects the 'default' keyword argument
        from contextvars import ContextVar
        my_var = ContextVar('my_var', [])

    def dict_fromkeys_chained_non_constructor_call():
        # A call that happens to return a list but is not a recognised constructor
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, sorted([3, 1, 2]))

    def contextvar_mutable_from_non_constructor():
        # A function that returns a list but is not a recognised mutable constructor
        from contextvars import ContextVar
        def make_list():
            return [1, 2, 3]
        my_var = ContextVar('my_var', default=make_list())

    def dict_fromkeys_nested_mutable_in_tuple():
        # The default is a tuple (immutable), even though it contains a list —
        # the outer container determines immutability for this check
        keys = ['a', 'b', 'c']
        my_dict = dict.fromkeys(keys, ([],))

    def contextvar_inside_class():
        from contextvars import ContextVar

        class MyService:
            state: ContextVar = ContextVar('state', default=[])  # Noncompliant
            #                                               ^^
            config: ContextVar = ContextVar('config', default={})  # Noncompliant
            #                                                 ^^

    def dict_fromkeys_inside_nested_function():
        def build_mapping(key_list):
            return dict.fromkeys(key_list, set())  # Noncompliant
            #                              ^^^^^
