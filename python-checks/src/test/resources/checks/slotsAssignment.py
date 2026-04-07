class UserBasic:
    __slots__ = ['name', 'email']

    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age  # Noncompliant {{Add "age" to the class's "__slots__".}}
#            ^^^


# Multiple missing attributes in same __init__
class UserMultipleMissing:
    __slots__ = ['name']

    def __init__(self, name, email, age):
        self.name = name
        self.email = email  # Noncompliant {{Add "email" to the class's "__slots__".}}
#            ^^^^^
        self.age = age  # Noncompliant {{Add "age" to the class's "__slots__".}}
#            ^^^


# Missing attribute in a non-__init__ method
class Point:
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_z(self, z):
        self.z = z  # Noncompliant {{Add "z" to the class's "__slots__".}}
#            ^


# __slots__ as tuple
class PointTuple:
    __slots__ = ('x', 'y')

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z  # Noncompliant {{Add "z" to the class's "__slots__".}}
#            ^


# Empty __slots__
class EmptySlots:
    __slots__ = []

    def __init__(self, value):
        self.value = value  # Noncompliant
#            ^^^^^


# Missing attribute in a property setter
class TemperatureWithBadCache:
    __slots__ = ['_celsius']

    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5 / 9
        self._fahrenheit_cache = value  # Noncompliant
#            ^^^^^^^^^^^^^^^^^


# Augmented assignment not in __slots__
class Counter:
    __slots__ = ['count']

    def __init__(self):
        self.count = 0

    def increment(self):
        self.total += 1  # Noncompliant
#            ^^^^^


# __slots__ as dict
class LinkedNode:
    __slots__ = {'value': 'The node value', 'next': 'The next node'}

    def __init__(self, value, next_node=None, extra=None):
        self.value = value
        self.next = next_node
        self.extra = extra  # Noncompliant
#            ^^^^^


# Assignment inside a conditional block
class Config:
    __slots__ = ['host', 'port']

    def __init__(self, host, port, debug=False):
        self.host = host
        self.port = port
        if debug:
            self.debug_info = "enabled"  # Noncompliant
#                ^^^^^^^^^^


# Subclass — attribute not in current or parent __slots__
class Base:
    __slots__ = ['base_attr']

    def __init__(self):
        self.base_attr = 1


class DerivedMissingAttr(Base):
    __slots__ = ['derived_attr']

    def __init__(self):
        super().__init__()
        self.derived_attr = 2
        self.other_attr = 3  # Noncompliant
#            ^^^^^^^^^^


# Augmented assignment not in any class's __slots__
class BaseWithCount:
    __slots__ = ['count']

    def __init__(self):
        self.count = 0


class DerivedAugmented(BaseWithCount):
    __slots__ = ['name']

    def update(self):
        self.count += 1  # Compliant: in parent slots
        self.missing += 1  # Noncompliant
#            ^^^^^^^


# Assignment inside a loop body
class Accumulator:
    __slots__ = ['total']

    def __init__(self):
        self.total = 0

    def process(self, items):
        for item in items:
            self.total += item
            self.last_item = item  # Noncompliant
#                ^^^^^^^^^


# Non-standard self parameter name
class WeirdSelf:
    __slots__ = ['value']

    def __init__(this, value):
        this.value = value
        this.extra = 42  # Noncompliant
#            ^^^^^


# Chained assignment — second target not in __slots__
class MultiAssign:
    __slots__ = ['x']

    def setup(self):
        self.x = self.y = 0  # Noncompliant
#                     ^


# Compliant: all attributes in __slots__
class UserCompliant:
    __slots__ = ['name', 'email', 'age']

    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age


# Compliant: no __slots__ means no restriction
class NoSlots:
    def __init__(self, name, value, extra):
        self.name = name
        self.value = value
        self.extra = extra
        self.anything = True


# Compliant: assigning to other.attr (not self)
class NodeCompliant:
    __slots__ = ['value', 'next']

    def __init__(self, value):
        self.value = value
        self.next = None

    def append(self, other):
        other.value = self.value
        other.next = None
        other.extra = 42


# Compliant: parent without __slots__ provides __dict__ to child
class ParentWithoutSlots:
    def __init__(self):
        self.parent_value = 0


class ChildInheritsDict(ParentWithoutSlots):
    __slots__ = ['extra']

    def __init__(self):
        super().__init__()
        self.extra = 1
        self.anything = True  # Compliant: parent provides __dict__


# Compliant: __slots__ contains '__dict__'
class WithDictSlot:
    __slots__ = ['name', '__dict__']

    def __init__(self, name):
        self.name = name
        self.dynamic_attr = "anything goes"
        self.other = 42


# Compliant: current + parent slots cover all assignments
class ShapeBase:
    __slots__ = ['color']

    def __init__(self, color):
        self.color = color


class Circle(ShapeBase):
    __slots__ = ['radius']

    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

    def scale(self, factor):
        self.radius *= factor


# Compliant: @staticmethod skipped
class MathHelper:
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value

    @staticmethod
    def add(a, b):
        result = a + b
        return result


# Compliant: @classmethod skipped
class Registry:
    __slots__ = ['name']

    def __init__(self, name):
        self.name = name

    @classmethod
    def create(cls, name):
        obj = cls.__new__(cls)
        return obj


# Compliant: tuple __slots__ covers all attributes
class PointTupleCompliant:
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


# Compliant: dict __slots__ covers all attributes
class LinkedNodeCompliant:
    __slots__ = {'value': 'The node value', 'next': 'The next node'}

    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


# Compliant: property setter assigns only to slots attributes
class TemperatureCompliant:
    __slots__ = ['_celsius']

    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5 / 9


# FN accepted: dynamic __slots__ — rule bails
def compute_slots():
    return ['x', 'y']


class DynamicSlots:
    __slots__ = compute_slots()

    def __init__(self):
        self.x = 1
        self.z = 2  # FN: __slots__ not a literal


# Compliant: qualifier is subscript, not a name
class NoParams:
    __slots__ = ['value']

    def unusual_method(*args):
        args[0].value = 1
        args[0].extra = 2


# Compliant: nested function not analyzed
class WithNestedFunction:
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value

        def inner(self):
            self.anything = True  # not visited


# FN accepted: indirect self reference not tracked
class SelfAlias:
    __slots__ = ['value']

    def __init__(self):
        obj = self
        obj.value = 1
        obj.missing = 2  # FN: qualifier is 'obj'


# Compliant: qualifier of 'value' is 'self.child', not 'self'
class DeepChain:
    __slots__ = ['child']

    def __init__(self):
        self.child = None
        self.child.value = 10


# Compliant: __dict__ in __slots__ lifts restriction
class OnlyDictSlot:
    __slots__ = ['__dict__']

    def __init__(self):
        self.anything = True
        self.more = "hello"


# Compliant: grandparent has no __slots__, __dict__ available
class GrandParentNoSlots:
    pass


class ParentWithSlots(GrandParentNoSlots):
    __slots__ = ['parent_val']


class GrandChildWithSlots(ParentWithSlots):
    __slots__ = ['child_val']

    def __init__(self):
        self.child_val = 1
        self.parent_val = 2
        self.anything = 3  # Compliant: grandparent provides __dict__


# Variable references in __slots__ resolved via single-assignment analysis
SLOT_NAME = 'value'


class NonStringSlots:
    __slots__ = [SLOT_NAME, 'other']

    def __init__(self):
        self.value = 1
        self.missing = 2  # Noncompliant {{Add "missing" to the class's "__slots__".}}
#            ^^^^^^^


class NonStringTupleSlots:
    __slots__ = (SLOT_NAME, 'other')

    def __init__(self):
        self.value = 1
        self.missing = 2  # Noncompliant {{Add "missing" to the class's "__slots__".}}
#            ^^^^^^^


# FN accepted: dict unpacking element in __slots__ dict — rule bails
extra = {'z': 'extra'}


class DictUnpackingSlots:
    __slots__ = {'x': 'x coord', **extra}

    def __init__(self):
        self.x = 1
        self.missing = 2  # FN: unpacking in __slots__ dict


# FN accepted: non-string key in __slots__ dict — rule bails
class NonStringKeyDictSlots:
    __slots__ = {1: 'one', 'other': 'two'}

    def __init__(self):
        self.other = 1
        self.missing = 2  # FN: non-string key in __slots__ dict


# Compliant: class has unresolved type hierarchy (inherits from unknown external class)
from unknown_module import ExternalBase  # noqa


class InheritsFromUnknown(ExternalBase):
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value
        self.extra = 42  # Compliant: unresolved hierarchy, rule bails


# Compliant: method with only keyword-only parameters (no positional params)
class KeywordOnlyMethod:
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value

    def update(self, *, kwarg):
        result = kwarg
        return result


# Compliant: chained __slots__ assignment (lhsExpressions.size() > 1) — rule bails
class ChainedSlotsAssignment:
    __slots__ = other_var = ['value']

    def __init__(self):
        self.value = 1
        self.extra = 2  # FN: chained assignment makes __slots__ unrecognized


# Compliant: tuple-unpack LHS on __slots__ assignment (lhs.size() != 1) — rule bails
class TupleUnpackLhsSlots:
    a, b = 1, 2  # lhs expressions list has 2 elements, skipped
    __slots__ = ['value']

    def __init__(self):
        self.value = 1


# Compliant: LHS is a list literal wrapping a name (lhs.size() == 1, not a NAME) — rule bails
class ListWrapLhsSlots:
    [__slots__] = [['value']]

    def __init__(self):
        self.value = 1
        self.extra = 2  # FN: list-wrap LHS makes __slots__ unrecognized


# Compliant: non-__slots__ assignment in class body does not confuse the check
class WithOtherClassVar:
    class_var = 42
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value


# Compliant: parent has __dict__ in its __slots__, providing __dict__ to child
class ParentWithDictSlot:
    __slots__ = ['parent_val', '__dict__']

    def __init__(self):
        self.parent_val = 0


class ChildOfParentWithDictSlot(ParentWithDictSlot):
    __slots__ = ['child_val']

    def __init__(self):
        super().__init__()
        self.child_val = 1
        self.anything = True  # Compliant: parent has __dict__ in slots


# Compliant: explicit object inheritance — object is skipped in ancestor collection
class ExplicitObjectBase(object):
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value


# Inherits from built-in list — external parent has no local ClassDef
class InheritsFromBuiltin(list):
    __slots__ = ['label']

    def __init__(self, label):
        super().__init__()
        self.label = label
        self.extra = 42  # Noncompliant


# Compliant: method with no parameters at all (parameterList is null -> positional params empty)
class NoParamMethod:
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value

    def no_params():
        pass


# Compliant: LHS in class body is a subscript (not a Name) — skipped by extractOwnSlots
class LhsSubscriptInBody:
    _registry = {}
    _registry['key'] = 'registered'
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value


# Compliant: parent is a dynamically-assigned name with no FQN — skipped in ancestor collection
def make_dynamic_base():
    class _Inner:
        __slots__ = ['x']
    return _Inner


DynamicBase = make_dynamic_base()


class InheritsDynamicBase(DynamicBase):
    __slots__ = ['y']

    def __init__(self, x, y):
        self.x = x  # Compliant: DynamicBase parent is skipped (fqn is null)
        self.y = y


# Compliant: class with ambiguous symbol (defined in both branches) — getClassSymbolFromDef returns null
import sys as _sys

if _sys.version_info[0] >= 3:
    class VersionedClass:
        __slots__ = ['x']

        def __init__(self):
            self.x = 1
else:
    class VersionedClass:  # noqa
        __slots__ = ['x']

        def __init__(self):
            self.x = 1


# Compliant: parent class is ambiguously defined (same FQN) — parentClassSymbol is null
if _sys.version_info[0] >= 3:
    class AmbiguousParent:
        __slots__ = ['parent_val']
else:
    class AmbiguousParent:  # noqa
        __slots__ = ['parent_val']


class InheritsAmbiguousParent(AmbiguousParent):
    __slots__ = ['child_val']

    def __init__(self):
        self.parent_val = 1
        self.child_val = 2


# __slots__ as set literal — now supported
class SetSlots:
    __slots__ = {'name', 'value'}

    def __init__(self, name, value, extra):
        self.name = name
        self.value = value
        self.extra = extra  # Noncompliant {{Add "extra" to the class's "__slots__".}}
#            ^^^^^


# Compliant: set literal __slots__ covers all attributes
class SetSlotsCompliant:
    __slots__ = {'x', 'y', 'z'}

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


# Variable reference in set literal __slots__ resolved via single-assignment analysis
class NonStringSetSlots:
    __slots__ = {SLOT_NAME, 'other'}

    def __init__(self):
        self.other = 1
        self.missing = 2  # Noncompliant {{Add "missing" to the class's "__slots__".}}
#            ^^^^^^^


# __slots__ as single string — now supported
class SingleStringSlots:
    __slots__ = 'value'

    def __init__(self, value, extra):
        self.value = value
        self.extra = extra  # Noncompliant {{Add "extra" to the class's "__slots__".}}
#            ^^^^^


# Compliant: single string __slots__ covers the attribute
class SingleStringSlotsCompliant:
    __slots__ = 'value'

    def __init__(self, value):
        self.value = value


# Multiple __slots__ assignments — last one wins
class MultipleSlotsAssignments:
    __slots__ = ['x', 'y', 'z']
    __slots__ = ['x']

    def __init__(self):
        self.x = 1
        self.y = 2  # Noncompliant {{Add "y" to the class's "__slots__".}}
#            ^


# Multiple __slots__ assignments — last one is larger
class MultipleSlotsLarger:
    __slots__ = ['x']
    __slots__ = ['x', 'y', 'z']

    def __init__(self):
        self.x = 1
        self.y = 2
        self.z = 3


# Compliant: nested class inside method does not cause false positives
class OuterWithNestedClass:
    __slots__ = ['x']

    def method(self):
        self.x = 1
        class Inner:
            def __init__(inner_self):
                inner_self.y = 1  # Compliant: visitor stops at nested class


# Diamond inheritance — slots from all branches are allowed
class DiamondBase:
    __slots__ = ['base_attr']

class DiamondLeft(DiamondBase):
    __slots__ = ['left_attr']

class DiamondRight(DiamondBase):
    __slots__ = ['right_attr']

class DiamondChild(DiamondLeft, DiamondRight):
    __slots__ = ['child_attr']

    def __init__(self):
        self.base_attr = 1   # Compliant: from DiamondBase via DiamondLeft
        self.left_attr = 2   # Compliant: from DiamondLeft
        self.right_attr = 3  # Compliant: from DiamondRight
        self.child_attr = 4  # Compliant: own slot
        self.missing = 5     # Noncompliant {{Add "missing" to the class's "__slots__".}}
#            ^^^^^^^

# Compliant: parent class from different file — can't determine its __slots__
from collections import OrderedDict

class CustomOrderedDict(OrderedDict):
    __slots__ = ['label']

    def __init__(self, label):
        super().__init__()
        self.label = label
        self.extra = 42  # Compliant: can't inspect external parent's __slots__


# FN accepted: empty tuple __slots__
class EmptyTupleSlots:
    __slots__ = ()

    def __init__(self, value):
        self.value = value  # Noncompliant {{Add "value" to the class's "__slots__".}}
#            ^^^^^


# FN accepted: function call element in __slots__ list — rule bails
class FuncCallInSlots:
    __slots__ = ['name', some_func()]

    def __init__(self):
        self.name = 1
        self.missing = 2  # FN: function call in __slots__ list


# FN accepted: integer literal element in __slots__ list — rule bails
class IntLiteralInSlots:
    __slots__ = ['name', 42]

    def __init__(self):
        self.name = 1
        self.missing = 2  # FN: non-string literal in __slots__ list


# FN accepted: star-unpacking element in __slots__ list — rule bails
base_slots = ['x', 'y']


class StarUnpackingInSlots:
    __slots__ = [*base_slots, 'z']

    def __init__(self):
        self.z = 1
        self.missing = 2  # FN: star-unpacking in __slots__ list


# FN accepted: unresolvable variable in __slots__ — rule bails
from unknown_module import EXTERNAL_SLOT  # noqa


class UnresolvableVarInSlots:
    __slots__ = ['name', EXTERNAL_SLOT]

    def __init__(self):
        self.name = 1
        self.missing = 2  # FN: variable can't be resolved


# FN accepted: variable resolves to non-string value — rule bails
MY_INT_VAR = 42


class VarResolvesToNonString:
    __slots__ = ['name', MY_INT_VAR]

    def __init__(self):
        self.name = 1
        self.missing = 2  # FN: variable resolves to int, not string


# FN accepted: variable assigned multiple times — rule bails
if _sys.version_info[0] >= 3:
    AMBIGUOUS_SLOT = 'x'
else:
    AMBIGUOUS_SLOT = 'y'


class AmbiguousVarInSlots:
    __slots__ = ['name', AMBIGUOUS_SLOT]

    def __init__(self):
        self.name = 1
        self.missing = 2  # FN: variable has multiple assignments


# FN accepted: concatenation expression in __slots__ — rule bails
class ConcatenatedSlots:
    __slots__ = ['x'] + ['y']

    def __init__(self):
        self.x = 1
        self.missing = 2  # FN: __slots__ is a binary expression, not a literal

# Compliant: __slots__ uses mangled names and assignments use double-underscore syntax
class Rat(object):
    __slots__ = ['_Rat__num', '_Rat__den']

    def __init__(self, num=0, den=1):
        self.__num = num  # Compliant: stored as _Rat__num, which is in __slots__
        self.__den = den  # Compliant: stored as _Rat__den, which is in __slots__


# Issue raised when attribute is not in slots even with partial mangled entries
class RatMissing(object):
    __slots__ = ['_RatMissing__num']

    def __init__(self, num=0, den=1):
        self.__num = num  # Compliant: stored as _RatMissing__num, which is in __slots__
        self.__den = den  # Noncompliant {{Add "__den" to the class's "__slots__".}}
#            ^^^^^


# Compliant: class name starts with underscore — mangling strips leading underscores from class name
# Python mangles _Rat.__den to _Rat__den (not __Rat__den)
class _Rat(object):
    __slots__ = ['_Rat__num', '_Rat__den']

    def __init__(self, num=0, den=1):
        self.__num = num  # Compliant: stored as _Rat__num, which is in __slots__
        self.__den = den  # Compliant: stored as _Rat__den, which is in __slots__
