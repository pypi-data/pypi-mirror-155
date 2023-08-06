import functools
import json

import attr
import cattr

from python_qa.utils.func import func_parameters
from python_qa.utils.classes import is_attrs_class
from requests import Response

from python_qa.utils.random import logger

from python_qa.utils.func import func_args_dict


def throw_response_missmatch(
        fields: dict, resp: Response, exception: Exception
):
    raise TypeError(
        f"Parameters miss-matched. "
        f"First level: "
        f"\n\tExpect: {sorted(fields)}"
        f"\n\tActual: {sorted(resp.json().keys())}"
        f"\n\tOriginal exception: {exception}"
    )


class Decorators:
    @staticmethod
    def request_typing(response_type=None, client_error_type=None):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                f_args = func_args_dict(func, *args, **kwargs)
                data = f_args.get("data", None)
                params = f_args.get("params", None)
                if is_attrs_class(data):
                    data = cattr.unstructure(data)
                    f_args["data"] = json.dumps(data)
                elif isinstance(data, list) and is_attrs_class(data[0]):
                    list_data = []
                    for d in data:
                        list_data.append(cattr.unstructure(d))
                    f_args["data"] = json.dumps(list_data)
                if is_attrs_class(params):
                    f_args["params"] = cattr.unstructure(params)
                args = f_args.values()
                resp = func(*args, **kwargs)
                if response_type and resp.status_code // 100 == 2:
                    try:
                        resp.typed = cattr.structure(resp.json(), response_type)
                    except (TypeError, ValueError, KeyError) as exp:
                        fields = attr.fields_dict(response_type)
                        throw_response_missmatch(fields, resp, exp)
                elif client_error_type and resp.status_code // 100 == 4:
                    resp.typed = cattr.structure(resp.json(), client_error_type)
                return resp
            return wrapper
        return decorator

    @staticmethod
    def step(title: str = None):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                params = func_parameters(func, *args, **kwargs)
                try:
                    params_title = title.format(*args, **params)
                except KeyError:
                    params_title = title
                logger.info("Executing: " + params_title)
                return func(*args, **kwargs)

            return wrapper

        return decorator


deco = Decorators
