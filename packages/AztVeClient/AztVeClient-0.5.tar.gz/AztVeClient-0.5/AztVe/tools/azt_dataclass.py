import dataclasses
import datetime
from . import azt_errors


def _verify_params(param, verify_type, default=None):
    if not isinstance(param, verify_type):
        return default
    return param


def aztdataclass(protocls,
                 price_dec: str = None, amount_dec: str = None,
                 adj_price: list = None, adj_amount: list = None,
                 adj_repeat: list = None, adj_repeat_price: list = None, adj_repeat_amount: list = None,
                 adj_map: list = None, adj_map_price: list = None, adj_map_amount: list = None,
                 adj_time: dict = None,
                 **kwargs
                 ):
    # 1 参数类型验证
    price_dec = _verify_params(price_dec, str)
    amount_dec = _verify_params(amount_dec, str)

    adj_price = _verify_params(adj_price, list)
    adj_amount = _verify_params(adj_amount, list)

    adj_repeat = _verify_params(adj_repeat, list)
    adj_repeat_price = _verify_params(adj_repeat_price, list)
    adj_repeat_amount = _verify_params(adj_repeat_amount, list)

    adj_map = _verify_params(adj_map, list)
    adj_map_price = _verify_params(adj_map_price, list)
    adj_map_amount = _verify_params(adj_map_amount, list)

    adj_time = _verify_params(adj_time, dict)

    # 2 将列表转为集合
    adj_price_attrs = set() if adj_price is None else set(adj_price)
    adj_amount_attr = set() if adj_amount is None else set(adj_amount)

    adj_repeat_attrs = set() if adj_repeat is None else set(adj_repeat)
    adj_repeat_price_attrs = set() if adj_repeat_price is None else set(adj_repeat_price)
    adj_repeat_amount_attrs = set() if adj_repeat_amount is None else set(adj_repeat_amount)

    adj_map_attrs = set() if adj_map is None else set(adj_map)
    adj_map_price_attrs = set() if adj_map_price is None else set(adj_map_price)
    adj_map_amount_attrs = set() if adj_map_amount is None else set(adj_map_amount)

    adj_time_attrs = set() if adj_time is None else set(adj_time)

    # 3 获取需要处理的属性集合
    abnormal_attrs = adj_price_attrs | adj_amount_attr | adj_repeat_attrs | adj_repeat_price_attrs \
                     | adj_repeat_amount_attrs | adj_map_attrs | adj_map_price_attrs | adj_map_amount_attrs \
                     | adj_time_attrs

    # 4 获取小数位数据
    price_decimal_place = _verify_params(kwargs.get("pdp"), int, 2)
    amount_decimal_place = _verify_params(kwargs.get("adp"), int, 2)
    price_decimal_pow = 10 ** price_decimal_place
    amount_decimal_pow = 10 ** amount_decimal_place

    def func_proto2py(cls, proto):
        params = dict()

        cls_attrs = cls.__annotations__
        # 1 不需要处理的属性
        normal_attrs = set(cls_attrs.keys()) - abnormal_attrs
        for normal_attr_name in normal_attrs:
            if hasattr(proto, normal_attr_name):
                normal_atrr_cls = cls_attrs[normal_attr_name]
                if hasattr(normal_atrr_cls, "__proto2py__"):
                    params[normal_attr_name] = normal_atrr_cls.__proto2py__(getattr(proto, normal_attr_name))
                else:
                    params[normal_attr_name] = getattr(proto, normal_attr_name)
        # 2 需要处理的属性
        # 2.1 需要由int转float的价格
        if price_dec is not None:
            p_d = 1
            if hasattr(proto, price_dec):
                proto_pd = getattr(proto, price_dec)
                p_d = (10 ** proto_pd) if isinstance(proto_pd, int) else p_d
            # int转float的价格
            for price_attr_name in adj_price_attrs:
                if hasattr(proto, price_attr_name):
                    params[price_attr_name] = getattr(proto, price_attr_name) / p_d
            # repeat转list,需要将价格由int转float
            for repeat_price_attr_name in adj_repeat_price_attrs:
                if hasattr(proto, repeat_price_attr_name):
                    params[repeat_price_attr_name] = [inner_price / p_d for inner_price in
                                                      getattr(proto, repeat_price_attr_name)]
            # todo map price

        if amount_dec is not None:
            a_d = 1
            if hasattr(proto, amount_dec):
                proto_ad = getattr(proto, amount_dec)
                a_d = (10 ** proto_ad) if isinstance(proto_ad, int) else a_d
            # int转float的数额
            for amount_attr_name in adj_amount_attr:
                if hasattr(proto, amount_attr_name):
                    params[amount_attr_name] = getattr(proto, amount_attr_name) / a_d
            # repeat转list,需要将数额由int转float
            for repeat_amount_attr_name in adj_repeat_amount_attrs:
                if hasattr(proto, repeat_amount_attr_name):
                    params[repeat_amount_attr_name] = [inner_amount / a_d for inner_amount in
                                                       getattr(proto, repeat_amount_attr_name)]
            # todo map amount

        # 2.3 repeat转list,需要考虑是否为自定义类型
        for repeat_attr_name in adj_repeat_attrs:
            if hasattr(proto, repeat_attr_name):
                repeat_attr_cls = cls_attrs[repeat_attr_name]
                if type(repeat_attr_cls) is list:
                    inner_type = repeat_attr_cls[0]
                    if hasattr(inner_type, "__proto2py__"):
                        params[repeat_attr_name] = [inner_type.__proto2py__(inner_proto) for inner_proto in
                                                    getattr(proto, repeat_attr_name)]
                    else:
                        params[repeat_attr_name] = list(getattr(proto, repeat_attr_name))
                else:
                    params[repeat_attr_name] = list(getattr(proto, repeat_attr_name))

        # todo map转dict
        # 未完待续
        # 时间格式转换
        for time_attr_name in adj_time_attrs:
            if hasattr(proto, time_attr_name):
                proto_time_attr_val: str = getattr(proto, time_attr_name)
                if proto_time_attr_val != "":
                    time_format = adj_time[time_attr_name]
                    params[time_attr_name] = datetime.datetime.strptime(proto_time_attr_val, time_format)
        return cls(**params)

    # # todo py转proto方法 未完待续...
    def func_py2proto(self):
        proto = protocls()
        cls_attrs = self.__annotations__
        # 1 不需要处理的属性
        normal_attrs = set(cls_attrs.keys()) - abnormal_attrs
        for normal_attr_name in normal_attrs:
            if hasattr(proto, normal_attr_name):
                normal_attr_val = getattr(self, normal_attr_name)
                if normal_attr_val is not None:
                    if hasattr(normal_attr_val, "__py2proto__"):
                        setattr(proto, normal_attr_name, normal_attr_val.__py2proto__())
                    else:
                        setattr(proto, normal_attr_name, normal_attr_val)
        # 2 需要由float转回int的属性
        if price_dec is not None:
            if hasattr(proto, price_dec):
                setattr(proto, price_dec, price_decimal_place)
            for price_attr_name in adj_price_attrs:
                if hasattr(proto, price_attr_name):
                    price_attr_val = getattr(self, price_attr_name)
                    if price_attr_val is not None:
                        setattr(proto, price_attr_name, int(price_attr_val * price_decimal_pow))
            for repeat_price_attr_name in adj_repeat_price_attrs:
                if hasattr(proto, repeat_price_attr_name):
                    repeat_price_attr_val = getattr(self, repeat_price_attr_name)
                    if isinstance(repeat_price_attr_val, list):
                        getattr(proto, repeat_price_attr_name).extend(
                            [repeat_price * price_decimal_pow for repeat_price in repeat_price_attr_val]
                        )
            # todo : for price map
        if amount_dec is not None:
            if hasattr(proto, amount_dec):
                setattr(proto, amount_dec, amount_decimal_place)
            for amount_attr_name in adj_amount_attr:
                if hasattr(proto, amount_attr_name):
                    amount_attr_val = getattr(self, amount_attr_name)
                    if amount_attr_val is not None:
                        setattr(proto, amount_attr_name, int(amount_attr_val * amount_decimal_pow))
            for repeat_amount_attr_name in adj_repeat_amount_attrs:
                if hasattr(proto, repeat_amount_attr_name):
                    repeat_amount_attr_val = getattr(self, repeat_amount_attr_name)
                    if repeat_amount_attr_val:
                        getattr(proto, repeat_amount_attr_name).extend(
                            [repeat_amount * amount_decimal_pow for repeat_amount in repeat_amount_attr_val]
                        )
            # todo : for amount map
        # 3 repeat
        for repeat_attr_name in adj_repeat_attrs:
            if hasattr(proto, repeat_attr_name):
                repeat_attr_cls = cls_attrs[repeat_attr_name]
                if type(repeat_attr_cls) is list:
                    inner_type = repeat_attr_cls[0]
                    if hasattr(inner_type, "__py2proto__"):
                        repeat_attr_val = getattr(self, repeat_attr_name)
                        getattr(proto, repeat_attr_name).extend(
                            [repeat_val.__py2proto__() for repeat_val in repeat_attr_val]
                        )
                    else:
                        getattr(proto, repeat_attr_name).extend(getattr(self, repeat_attr_name))
            else:
                raise azt_errors.ListTypeError
        # 4 todo map
        # 5 时间格式转换
        for time_attr_name in adj_time_attrs:
            if hasattr(proto, time_attr_name):
                time_attr_val = getattr(self, time_attr_name)
                if time_attr_val is None:
                    continue
                if isinstance(time_attr_val, datetime.datetime):
                    time_format = adj_time[time_attr_name]
                    setattr(proto, time_attr_name, time_attr_val.strftime(time_format))
                elif isinstance(time_attr_val, str):
                    setattr(proto, time_attr_name, time_attr_val)
                else:
                    raise azt_errors.DatetimeTypeError
        return proto

    def wrapper_func(pycls):
        if not hasattr(pycls, "__proto2py__"):
            setattr(pycls, "__proto2py__", classmethod(func_proto2py))
        if not hasattr(pycls, "__py2proto__"):
            setattr(pycls, "__py2proto__", func_py2proto)
        return dataclasses.dataclass(pycls)

    return wrapper_func
