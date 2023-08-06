import inspect
import typing
import random as rnd
from dataclasses import is_dataclass, MISSING
import datetime

import attr
from faker import Faker

from ..utils.data import DataGenerate
from ..logging.logging import Logging
from ..utils.classes import is_attrs_class, is_union_type, has_args, is_tuple, is_sequence
from ..types.base_types import *

logger = Logging.logger

T = typing.TypeVar("T")


class Randomer:
    _types = {}

    def get_func(self, t: T):
        func = self._types.get(t)
        if func:
            return func
        raise TypeError(f"Not found func for random {t} type data")

    def run_func(self, t: T, **kwargs):
        func = self.get_func(t)
        if inspect.getfullargspec(func).varkw:
            logger.debug(f"Parameters {kwargs} are passed to func")
            res = func(**kwargs)
        else:
            res = func()
        logger.debug(f"Data random for type {t}: {res}")
        return res

    def add_type(self, t: T, func: typing.Callable[[], T]):
        if t in self._types:
            logger.warning(f"Existing type {t} will be overriding")
        logger.debug(f"New type {t} with function {func} registering")
        self._types[t] = func

    def add_types(self, types: typing.Dict[T, typing.Callable[[], T]]):
        logger.debug(f"New types registered: {types}")
        self._types.update(types)

    def add_predefined(self, **kwargs):
        fake = Faker(**kwargs)
        types = {
            str: lambda: fake.sentence(2)[:-1],
            int: fake.pyint,
            float: fake.pyfloat,
            bool: fake.pybool,
            list: fake.pylist,
            Date: fake.date,
            Address: fake.address,
            Country: fake.country,
            CountryCode: fake.country_code,
            PostCode: fake.postcode,
            StreetAddress: fake.street_address,
            CarNumber: fake.license_plate,
            BBAN: fake.bban,
            IBAN: fake.iban,
            SWIFT11: fake.swift11,
            SWIFT8: fake.swift8,
            CreditCardExpire: fake.credit_card_expire,
            CreditCardNumber: fake.credit_card_number,
            CreditCardProvider: fake.credit_card_provider,
            CreditCardSecurityCode: fake.credit_card_security_code,
            CompanyName: fake.company,
            CompanySuffix: fake.company_suffix,
            FileName: fake.file_name,
            Ipv4: fake.ipv4,
            Ipv6: fake.ipv6,
            MacAddress: fake.mac_address,
            UserAgent: fake.user_agent,
            URI: fake.uri,
            Email: fake.email,
            Username: fake.user_name,
            FirstName: fake.first_name_male,
            LastName: fake.last_name_male,
            MiddleName: fake.middle_name_male,
            Password: fake.password,
            Patronymic: fake.middle_name_male,
            PhoneNumber: fake.phone_number,
            Job: fake.job,
            Paragraph: fake.paragraph,
            BusinessInn: fake.businesses_inn,
            IndividualInn: fake.individuals_inn,
            BusinessOgrn: fake.businesses_ogrn,
            IndividualOgrn: fake.individuals_ogrn,
            Kpp: fake.kpp,
            TimeStamp: lambda: fake.unix_time(
                start_datetime=(
                    datetime.date.today() - datetime.timedelta(days=30)
                )
            ),
            MongoId: DataGenerate.mongo_id,
        }
        self.add_types(types)

    def random_object(self, t: T, fields: typing.List[str] = [],
                      ignore_fields: bool = False,
                      save_defaults: bool = False,
                      **kwargs
                      ) -> T:
        data = {}
        if t in self._types:
            return self.run_func(t, **kwargs)
        elif is_attrs_class(t):
            for field in attr.fields(t):
                f_name = field.name
                has_default = field.default is not attr.NOTHING if save_defaults else None
                if f_name in kwargs:
                    data[f_name] = kwargs[f_name]
                    continue
                if (
                        (f_name in fields and ignore_fields) or
                        (save_defaults and has_default) or
                        (f_name not in fields and not ignore_fields and fields)
                ):
                    data[f_name] = field.default if has_default else None
                    continue
                data[f_name] = self.random_object(
                    field.type,
                    fields,
                    ignore_fields,
                    save_defaults,
                    **kwargs
                )
            logger.debug(f"Random data is generate for attrs type {data}")
            return t(**data)
        elif is_dataclass(t):
            for field in fields(t):
                f_name = field.name
                has_default = (
                    field.default is not MISSING
                    or field.default_factory is not MISSING
                ) if save_defaults else None
                if f_name in kwargs:
                    data[f_name] = kwargs[f_name]
                    continue
                if (
                        (f_name in fields and ignore_fields) or
                        (save_defaults and has_default) or
                        (f_name not in fields and not ignore_fields and fields)
                ):
                    data[f_name] = None
                    if has_default:
                        data[f_name] = (
                            field.default
                            if field.default != MISSING
                            else field.default_factory()
                        )
                    continue
                data[f_name] = self.random_object(
                    field.type,
                    fields,
                    ignore_fields,
                    save_defaults,
                    **kwargs
                )
            logger.debug(f"Random data is generate for dataclass type {data}")
            return t(**data)
        elif is_union_type(t) and has_args(t):
            return self.random_object(
                rnd.choice(t.__args__),
                fields,
                ignore_fields,
                save_defaults,
                **kwargs
            )
        elif is_tuple(t) and has_args(t):
            return (
                self.random_object(
                    t.__args__[0],
                    fields,
                    ignore_fields,
                    save_defaults,
                    **kwargs
                ),
            )
        elif is_sequence(t) and has_args(t):
            return [
                self.random_object(
                    rnd.choice(t.__args__),
                    fields,
                    ignore_fields,
                    save_defaults,
                    **kwargs
                )
            ]
        return None

    object = random_object
