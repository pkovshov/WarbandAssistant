import os
import warnings


__typechecker_value = os.environ.get("TYPECHECKER")
if not __typechecker_value or __typechecker_value == "BEAR":
    from beartype import beartype as typechecked
    from beartype.roar import BeartypeCallHintParamViolation as TypeCheckError
    warnings.filterwarnings("ignore", module="beartype")
elif __typechecker_value == "GUARD":
    from typeguard import typechecked
    from typeguard import TypeCheckError
elif __typechecker_value == "NONE":
    def typechecked(func):
        return func
    class TypeCheckError:
        pass
else:
    raise ValueError("env var TYPECHECKER must be NONE, GUARD, BEAR, empty or unset")
