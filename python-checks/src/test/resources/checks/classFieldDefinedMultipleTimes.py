class BasicDuplicate:
    x = 1  # Noncompliant {{Remove this assignment; "x" is assigned again on line 4.}}
#   ^
    x = 3
#   ^< {{Reassignment.}}
    y = 2


class CopyPasteError:
    width = 100  # Noncompliant {{Remove this assignment; "width" is assigned again on line 13.}}
#   ^^^^^
    height = 200
    width = 800
#   ^^^^^< {{Reassignment.}}


class RefactoringMistake:
    timeout = 30  # Noncompliant {{Remove this assignment; "timeout" is assigned again on line 21.}}
#   ^^^^^^^
    host = "localhost"
    timeout = 60
#   ^^^^^^^< {{Reassignment.}}


class AnnotatedThenPlain:
    x: int = 0  # Noncompliant {{Remove this assignment; "x" is assigned again on line 28.}}
#   ^
    x = 1
#   ^< {{Reassignment.}}


class MultipleDuplicatePairs:
    host = "localhost"  # Noncompliant
    port = 8080  # Noncompliant
    host = "production.example.com"
    port = 443


class ThreeAssignments:
    status = 0  # Noncompliant
    status = "pending"  # Noncompliant
    status = "active"


class NoneToValue:
    max_length = None  # Noncompliant
    max_results = 10
    max_length = 512


class BooleanFlip:
    enable_cache = False  # Noncompliant
    debug = True
    enable_cache = True


class TypeChange:
    code = 0  # Noncompliant
    code = "OK"


class AnnotatedThenAnnotated:
    value: int = 0  # Noncompliant
    value: int = 42


class DunderAttribute:
    __slots__ = []  # Noncompliant
    __slots__ = ["_name", "_value"]


class LiteralTypes:
    count = 0  # Noncompliant
    label = "initial"  # Noncompliant
    ratio = 0.5  # Noncompliant
    count = 100
    label = "final"
    ratio = 1.0


class UniqueFields:
    x = 1
    y = 2
    z = 3


class AugmentedAssignment:
    count = 0
    count += 1


class AnnotationOnlyThenAssignment:
    value: int
    value = 42


class ConditionalAssignments:
    debug = False
    if True:
        debug = True


class TryExceptPattern:
    backend = "redis"
    try:
        backend = "memcached"
    except ImportError:
        pass


class MethodSelfAssignments:
    name = "default"

    def __init__(self):
        self.name = "instance"

    def reset(self):
        self.name = "reset"


class ClassMethodAssignments:
    total = 0

    @classmethod
    def increment(cls):
        cls.total += 1


class ForLoopAssignment:
    items = []
    for i in range(10):
        items = [i]


class WithStatementAssignment:
    resource = None
    with open("file.txt") as f:
        resource = f.read()


class WhileLoopAssignment:
    retries = 0
    while retries < 3:
        retries = retries + 1


class TupleUnpacking:
    x = 0
    y = 0
    x, y = 1, 2


class ChainedAssignment:
    a = 0
    b = 0
    a = b = 5


class AttributeAssignment:
    x = 1
    SomeClass.x = 2


class SubscriptAssignment:
    data = {}
    data["key"] = "value"


class NestedClassSameName:
    x = 1

    class Inner:
        x = 10  # Noncompliant
        x = 20


class DifferentClasses:
    x = 1


class AnotherClass:
    x = 2


class NestedFunctionAssignment:
    field = "class_level"

    def setup(self):
        field = "local"
        field = "also_local"


class ComplexAnnotationNoValue:
    items: list[int]
    items: list[str]
    items = []


class SingleAnnotatedAssignment:
    version: str = "1.0.0"


class AugmentedAfterAnnotated:
    score: int = 0
    score += 10


class OnlyAnnotationsNoValues:
    x: int
    x: str


class PlainThenAnnotated:
    x = 1  # Noncompliant {{Remove this assignment; "x" is assigned again on line 216.}}
#   ^
    x: int = 42
#   ^< {{Reassignment.}}


class AnnotatedNonNameVariable:
    SomeClass.attr: int = 0
    data[0]: str = "x"


class SameValueAssignedTwice:
    _VERSION = "1.0"  # Noncompliant {{Remove this assignment; "_VERSION" is assigned again on line 232.}}
#   ^^^^^^^^
    _REQUEST_TOKEN_URL = "https://example.com/oauth/request_token"
    _ACCESS_TOKEN_URL = "https://example.com/oauth/access_token"
    _AUTHORIZE_URL = "https://example.com/oauth/authorize"
    _NO_CALLBACKS = True
    _VERSION = "1.0"
#   ^^^^^^^^< {{Reassignment.}}
