import collections
import inspect
import types


def represent(item):
    if isinstance(item, str):
        return f"'{item}'"
    elif isinstance(item, (bytes, bytearray)):
        return repr(type(item))
    elif isinstance(item, types.FunctionType):
        return inspect.getsource(item).strip()
    else:
        return repr(item)


def func_parameters(func, *args, **kwargs):
    parameters = {}
    args_spec = inspect.getfullargspec(func)
    args_order = list(args_spec.args)
    args_dict = dict(zip(args_spec.args, args))

    if args_spec.defaults:
        defaults = dict(
            zip(args_spec.args[len(args):], args_spec.defaults)
        )
        parameters.update(defaults)

    if args_spec.varargs:
        args_order.append(args_spec.varargs)
        varargs = args[len(args_spec.args):]
        parameters.update({args_spec.varargs: varargs} if varargs else {})

    if args_spec.args and args_spec.args[0] in ["cls", "self"]:
        args_dict.pop(args_spec.args[0], None)

    if kwargs:
        args_order.extend(list(kwargs.keys()))
        parameters.update(kwargs)

    parameters.update(args_dict)
    items = parameters.items()
    sorted_items = sorted(
        map(lambda k: (k[0], represent(k[1])), items),
        key=lambda x: args_order.index(x[0]),
    )

    return collections.OrderedDict(sorted_items)


def func_args_dict(func, *args):
    args_spec = inspect.getfullargspec(func)
    return dict(zip(args_spec.args, args))
