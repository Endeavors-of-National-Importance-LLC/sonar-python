numbers = [42, 17, 93, 8, 51]
words = ["banana", "fig", "apple", "date"]

# Issues detected
smallest = sorted(numbers)[0]  # Noncompliant {{Use "min()" instead of sorting to find this value.}}
#          ^^^^^^^^^^^^^^^^^^

largest = sorted(numbers)[-1]  # Noncompliant {{Use "max()" instead of sorting to find this value.}}
#         ^^^^^^^^^^^^^^^^^^^

also_largest = sorted(numbers, reverse=True)[0]  # Noncompliant {{Use "max()" instead of sorting to find this value.}}
#              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

also_smallest = sorted(numbers, reverse=True)[-1]  # Noncompliant {{Use "min()" instead of sorting to find this value.}}
#               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# reverse=False is treated the same as no reverse argument
x = sorted(numbers, reverse=False)[0]  # Noncompliant {{Use "min()" instead of sorting to find this value.}}
y = sorted(numbers, reverse=False)[-1]  # Noncompliant {{Use "max()" instead of sorting to find this value.}}

# key parameter does not suppress the issue
shortest = sorted(words, key=len)[0]  # Noncompliant {{Use "min()" instead of sorting to find this value.}}
#          ^^^^^^^^^^^^^^^^^^^^^^^^^

longest_by_len = sorted(words, key=len, reverse=True)[0]  # Noncompliant {{Use "max()" instead of sorting to find this value.}}

# inline collection literal
inline_min = sorted([5, 3, 8, 1])[0]  # Noncompliant

# used in a boolean expression
def get_min(data):
    if sorted(data)[0] < 0:  # Noncompliant
        return True


# Compliant cases

# use min() and max() directly
min_val = min(numbers)
max_val = max(numbers)
min_by_len = min(words, key=len)
max_by_len = max(words, key=len)

# sorted() without indexing
sorted_numbers = sorted(numbers)

# index other than 0 or -1
second = sorted(numbers)[1]
second_to_last = sorted(numbers)[-2]

# slice, not a single index
first_three = sorted(numbers)[0:3]

# indexing a non-sorted() object
first = numbers[0]
last = numbers[-1]

# sorted result stored in a variable first
ordered = sorted(numbers)
first_ordered = ordered[0]
last_ordered = ordered[-1]

# custom (shadowed) sorted function
def case_custom_sorted():
    def sorted(iterable):
        return list(iterable)
    result = sorted(numbers)[0]

# indirect call through a variable
def case_indirect():
    sort_fn = sorted
    result = sort_fn(numbers)[0] # Noncompliant
#            ^^^^^^^^^^^^^^^^^^^

# sorted result wrapped in another call
def identity(x):
    return x

wrapped = identity(sorted(numbers))[0]

# multiple subscripts (tuple index) - not a single subscript
multi_subscript = sorted(numbers)[0, 1]

# qualified name callee - TypeMatchers resolves builtins.sorted correctly
import builtins
qualified_sorted = builtins.sorted(numbers)[0]  # Noncompliant {{Use "min()" instead of sorting to find this value.}}

# unary plus index - not UNARY_MINUS, so not -1
unary_plus_index = sorted(numbers)[+1]

# unary minus applied to a variable - not a NumericLiteral operand
neg_var = 1
unary_minus_var_index = sorted(numbers)[-neg_var]

# reverse argument is a truthy integer literal
reverse_int_literal = sorted(numbers, reverse=1)[0]  # Noncompliant {{Use "max()" instead of sorting to find this value.}}

# reverse argument is a falsy integer literal
reverse_zero = sorted(numbers, reverse=0)[0]  # Noncompliant {{Use "min()" instead of sorting to find this value.}}

# reverse argument is a variable assigned to True - resolved through single assignment
rev_flag = True
reverse_var = sorted(numbers, reverse=rev_flag)[0]  # Noncompliant {{Use "max()" instead of sorting to find this value.}}

# reverse argument is an unknown variable - cannot determine truthiness, skip
def some_function(flag):
    unknown_reverse = sorted(numbers, reverse=flag)[0]

# sorted used inside a lambda expression (the sorted()[index] is still flagged)
get_last = lambda lst: sorted(lst, key=lambda m: m)[-1]  # Noncompliant {{Use "max()" instead of sorting to find this value.}}

# sorted result used as subscript key into another collection
d = {"a": 1, "b": 2, "c": 3}
value = d[sorted(d.keys())[-1]]  # Noncompliant {{Use "max()" instead of sorting to find this value.}}

# negated key lambda - sorted(key=lambda x: -f(x))[0] is still noncompliant
items = ["hi", "hello", "hey"]
negated_key = sorted(items, key=lambda s: -len(s))[0]  # Noncompliant {{Use "min()" instead of sorting to find this value.}}

# multi-line sorted call - same rule applies regardless of formatting
multi_line_min = sorted(  # Noncompliant {{Use "min()" instead of sorting to find this value.}}
    words,
    key=len,
)[0]

test_float = sorted(items)[0.5] 
