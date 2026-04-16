
def noncompliant_materialize_first(users):
    return list(users)[0]  # Noncompliant {{Replace "list(...)[0]" with "next(iter(...))" to avoid materializing the entire iterable.}}
#          ^^^^


def compliant_next_iter(users):
    return next(iter(users))

def compliant_nonzero_index(items):
    return list(items)[1]

def compliant_float_subscript(items):
    return list(items)[0.0]

def compliant_float_scientific_zero(items):
    return list(items)[0e0]

def compliant_complex_subscript(items):
    return list(items)[0j]

def compliant_negative_index(items):
    return list(items)[-1]

def compliant_slice(items):
    return list(items)[0:1]

def compliant_tuple_subscript(items):
    return list(items)[0, 1]

def compliant_starred(args):
    return list(*args)[0]

def compliant_multiple_args():
    return list([], [])[0]

def compliant_direct_index(items):
    return items[0]

def compliant_two_step_list(items):
    all_items = list(items)
    return all_items[0]  # out of scope: [0] applies to a Name, not to list(...) call

def compliant_shadowed_list(items):
    list = lambda x: x
    return list(items)[0]


def fn_subscript_not_literal_zero(items):
    zero = 0
    return list(items)[zero]  # FN: subscript must be numeric literal 0
