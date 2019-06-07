
import marshmallow
import sys
import types


# Patch marshmallow to provide marshmallow.compat which was removed in 3.0.0rc6.
# Current latest version of marshmallow-peewee still uses marshmallow.compat.

compat = types.ModuleType('compat')
marshmallow.compat = compat
sys.modules['marshmallow.compat'] = compat


def with_metaclass(meta, *bases):
    class MetaClass(meta):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

    return type.__new__(MetaClass, 'temporary_class', (), {})


compat.with_metaclass = with_metaclass
compat.PY2 = False
