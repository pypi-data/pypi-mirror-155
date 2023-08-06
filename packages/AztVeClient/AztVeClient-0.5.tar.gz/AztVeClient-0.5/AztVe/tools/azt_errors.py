# 尚未登录
class NotLoginedError(Exception):
    pass


# 非交易时间
class NonTradingTimeError(Exception):
    pass


# 时间格式错误
class DatetimeTypeError(TypeError):
    pass


# 列表格式错误
class ListTypeError(TypeError):
    pass


# 参数错误
class ArgsError(Exception):
    pass
