import typing


def filtered(func: typing.Callable, iterable: typing.Iterable):
    return type(iterable)(filter(func, iterable))
