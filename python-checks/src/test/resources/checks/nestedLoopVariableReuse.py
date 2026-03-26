def simple_shadowing():
    for i in range(10):
#       ^> {{Outer loop variable.}}
        for i in range(5):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "i".}}
#           ^
            pass


def long_variable_name_shadowing():
    for item in get_items():
#       ^^^^> {{Outer loop variable.}}
        for item in get_sub_items():  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "item".}}
#           ^^^^
            process(item)


def shadowing_with_intervening_code():
    for x in range(10):
#       ^> {{Outer loop variable.}}
        print(x)
        if some_condition():
            for x in range(3):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "x".}}
#               ^
                do_something(x)


def tuple_unpacking_shadows_outer():
    for i in range(10):
#       ^> {{Outer loop variable.}}
        for i, j in some_pairs():  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "i".}}
#           ^
            pass


def inner_shadows_outer_tuple_element():
    for i, j in some_pairs():
#       ^> {{Outer loop variable.}}
        for i in range(5):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "i".}}
#           ^
            pass


def three_levels_shadowing():
    for i in range(10):
#       ^> {{Outer loop variable.}}
        for i in range(5):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "i".}}
#           ^
            for i in range(3):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "i".}}
#               ^
                pass


def three_levels_innermost_shadows_two_outers():
    for i in range(10):
        for j in range(5):
#           ^> {{Outer loop variable.}}
            for j in range(3):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "j".}}
#               ^
                pass


def both_variables_shadow_respective_outers():
    for i in range(10):
        for j in range(5):
            for i, j in some_triples():  # Noncompliant 2
                pass


def shadowing_inside_with_block():
    for i in range(10):
#       ^> {{Outer loop variable.}}
        with open("file") as f:
            for i in range(5):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "i".}}
#               ^
                pass


def shadowing_inside_try_block():
    for n in range(10):
#       ^> {{Outer loop variable.}}
        try:
            for n in range(5):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "n".}}
#               ^
                pass
        except Exception:
            pass


def outer_loop_in_while_body():
    while True:
        for k in range(10):
#           ^> {{Outer loop variable.}}
            for k in range(5):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "k".}}
#               ^
                pass


def underscore_plus_real_variable_shadows():
    for k in range(10):
#       ^> {{Outer loop variable.}}
        for _, k in enumerate(items()):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "k".}}
#              ^
            pass


def async_for_shadows_regular_for():
    async def runner():
        for i in range(10):
#           ^> {{Outer loop variable.}}
            async for i in async_iterable():  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "i".}}
#                     ^
                pass


def underscore_variable_nested():
    for _ in range(10):
        for _ in range(5):  # _ is a throwaway variable, not flagged
            pass


def underscore_prefixed_variable_nested():
    for _item in range(10):
        for _item in range(5):  # _item starts with _, not flagged
            pass


def different_variable_names():
    for i in range(10):
        for j in range(5):
            pass


def consecutive_loops_same_name():
    for i in range(10):
        pass
    for i in range(5):
        pass


def inner_for_in_nested_function():
    for i in range(10):
        def helper():
            for i in range(5):
                pass
        helper()


def inner_for_in_nested_class():
    for i in range(10):
        class Helper:
            def method(self):
                for i in range(5):
                    pass


def inner_for_in_lambda():
    for i in range(10):
        transform = lambda i: i * 2
        results = list(map(transform, range(5)))


def inner_for_in_list_comprehension():
    for i in range(10):
        result = [i * 2 for i in range(5)]


def inner_for_in_set_comprehension():
    for i in range(10):
        result = {i for i in range(5)}


def inner_for_in_dict_comprehension():
    for i in range(10):
        result = {i: i * 2 for i in range(5)}


def inner_for_in_generator_expr():
    for i in range(10):
        result = sum(i for i in range(5))


def tuple_unpacking_no_clash():
    for i in range(10):
        for j, k in some_pairs():
            pass


def different_names_with_tuples():
    for a, b in some_pairs():
        for c, d in other_pairs():
            pass


def async_for_different_names():
    async def runner():
        for item in collection:
            async for sub_item in item.children():
                process(sub_item)


def single_loop_only():
    for i in range(10):
        do_something(i)


def deeply_nested_with_multiple_scope_boundaries():
    for i in range(10):
        class Outer:
            def method(self):
                for i in range(5):
                    def inner():
                        for i in range(3):
                            pass



def async_for_as_outer_shadows_inner():
    async def runner():
        async for i in async_iterable():
#                 ^> {{Outer loop variable.}}
            for i in range(5):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "i".}}
#               ^
                pass


def for_else_body_shadowing():
    for i in range(10):
#       ^> {{Outer loop variable.}}
        pass
    else:
        for i in range(5):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "i".}}
#           ^
            pass


def for_in_finally_shadows_outer():
    for i in range(10):
#       ^> {{Outer loop variable.}}
        try:
            do_something(i)
        finally:
            for i in range(5):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "i".}}
#               ^
                pass


def three_levels_skip_middle():
    for i in range(10):
#       ^> {{Outer loop variable.}}
        for j in range(5):
            for i in range(3):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "i".}}
#               ^
                pass


def outer_for_inside_with():
    with open("file") as f:
        for i in f:
#           ^> {{Outer loop variable.}}
            for i in range(5):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "i".}}
#               ^
                pass


def nested_tuple_element_shadows():
    for a, (b, c) in triples():
#           ^> {{Outer loop variable.}}
        for b in range(5):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "b".}}
#           ^
            pass


def for_in_except_body_shadows_outer():
    for n in range(10):
#       ^> {{Outer loop variable.}}
        try:
            do_something(n)
        except ValueError:
            for n in range(5):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "n".}}
#               ^
                pass



def async_for_as_outer_different_names():
    async def runner():
        async for item in async_iterable():
            for sub in range(5):
                process(item, sub)


def for_else_body_different_names():
    for i in range(10):
        pass
    else:
        for j in range(5):
            pass


def for_in_finally_different_names():
    for i in range(10):
        try:
            do_something(i)
        finally:
            for j in range(5):
                pass


def three_levels_no_clash():
    for i in range(10):
        for j in range(5):
            for k in range(3):
                pass


def nested_tuple_no_clash():
    for a, (b, c) in triples():
        for d in range(5):
            pass


def consecutive_loops_at_class_body_level():
    class MyClass:
        for i in range(10):
            pass
        for i in range(5):
            pass


def outer_for_inside_with_different_names():
    with open("file") as f:
        for line in f:
            for word in line.split():
                process(word)


def for_in_except_body_different_names():
    for n in range(10):
        try:
            do_something(n)
        except ValueError:
            for m in range(5):
                pass



def starred_variable_in_outer_for_not_detected():
    # STAR_EXPR targets are not extracted, so *b in outer loop is not tracked
    for a, *b in some_pairs():
        for b in range(5):
            pass


def starred_variable_in_inner_for_not_detected():
    # STAR_EXPR targets are not extracted from inner loop either
    for b in range(10):
        for a, *b in some_pairs():
            pass


def three_levels_scope_boundary_between_1_and_3():
    for i in range(10):
        def middle():
            for j in range(5):
                for i in range(3):  # not flagged — funcdef is a scope boundary
                    pass


def deeply_nested_tuple_variable_shadows():
    for a, (b, (c, d)) in deeply_nested():
#               ^> {{Outer loop variable.}}
        for c in range(5):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "c".}}
#           ^
            pass


def class_body_nested_loops_same_name():
    class MyClass:
        for i in range(10):
#           ^> {{Outer loop variable.}}
            for i in range(5):  # Noncompliant {{Rename this loop variable; it shadows the outer loop variable "i".}}
#               ^
                pass


def subscript_target_inner_loop_not_detected():
    for i in range(10):
        obj = {}
        for obj[i] in range(5):
            pass


def attribute_target_inner_loop_not_detected():
    for i in range(10):
        class C: pass
        c = C()
        for c.i in range(5):
            pass


for _module_item in range(10):
    pass
