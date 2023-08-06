import datetime
from ..tools.azt_dataclass import aztdataclass
from ..protobufs import Message_pb2 as proto


# ve账户注册请求
@aztdataclass(proto.RegisterReq)
class RegisterReq:
    strategy_id: str = None
    strategy_check_code: str = None


# ve账户登录请求
@aztdataclass(proto.LoginReq)
class LoginReq:
    account: str = None
    passwd: str = None


# ve账户登出请求
@aztdataclass(proto.LogoutReq)
class LogoutReq:
    account: str = None


# 账户信息查询请求
# account and passwd | strategy and check_code
# 若查询条件是 strategy_id + check_code，则返回 所有；
# 若查询条件是 account + passwd; 则只返回 account 和 acc_satus
@aztdataclass(proto.UserInfoQryReq)
class UserInfoQryReq:
    account: str = None
    passwd: str = None
    strategy_id: str = None
    strategy_check_code: str = None


# 账户入金请求
@aztdataclass(proto.AccDepositReq, amount_dec="amount_decimal_place", adj_amount=["amount"],
              adj_time=dict(sending_time="%Y%m%d-%H:%M:%S"))
class AccDepositReq:
    sender_user: str = None
    account: str = None
    client_ref: str = None
    amount: float = None
    sending_time: datetime.datetime = None


# 账户资金信息查询请求
@aztdataclass(proto.TradingAccQryReq)
class TradingAccQryReq:
    account: str = None


# 查询订单信息请求
# 除account外，皆可为空；
# client_ref 与 order_id 只填写一个即可, 则不填写market和code
# 查询未结委托，只填写 account 与 unfinished=true
@aztdataclass(proto.QueryOrdersReq)
class QueryOrdersReq:
    account: str = None  # 必填
    market: str = None  # 选填
    code: str = None  # 选填
    client_ref: str = None  # 选填,若填则无需填order_id、market和code
    order_id: str = None  # 选填,若填则无需填client_ref、market和code
    unfinished: bool = None  # 选填,若填则为查询未结委托,只需填写account与unfinished=true


# 查询交易信息请求
# 除account外，皆可为空
# trade_id 或 account market code order_id 填写，则无效（不用填写）
@aztdataclass(proto.QueryTradesReq)
class QueryTradesReq:
    account: str = None
    market: str = None
    code: str = None
    order_id: str = None
    trade_id: str = None


# 查询持仓请求
# 除account外，皆可为空
@aztdataclass(proto.QueryPositionsReq)
class QueryPositionsReq:
    account: str = None
    market: str = None
    code: str = None


# 查询历史订单记录请求
# market code 可空
@aztdataclass(proto.QueryHistoryOrdersReq, adj_time=dict(start_time="%Y%m%d-%H:%M:%S", end_time="%Y%m%d-%H:%M:%S"))
class QueryHistoryOrdersReq:
    account: str = None
    market: str = None
    code: str = None
    start_time: datetime.datetime = None
    end_time: datetime.datetime = None


# 查询历史交易记录请求
# market code 可空
@aztdataclass(proto.QueryHistoryTradesReq, adj_time=dict(start_time="%Y%m%d-%H:%M:%S", end_time="%Y%m%d-%H:%M:%S"))
class QueryHistoryTradesReq:
    account: str = None
    market: str = None
    code: str = None
    start_time: datetime.datetime = None
    end_time: datetime.datetime = None


# 委托订单请求
@aztdataclass(proto.PlaceOrder, price_dec="price_decimal_place", adj_price=["order_price", "discretion_price"],
              adj_time=dict(send_time="%Y%m%d-%H:%M:%S"))
class PlaceOrder:
    client_ref: str = None
    sender_user: str = None
    account: str = None
    market: str = None
    code: str = None
    order_type: int = None
    business_type: int = None
    order_side: int = None
    effect: int = None
    order_price: float = None
    order_qty: int = None
    order_id: str = None
    discretion_price: float = None
    send_time: datetime.datetime = None


# 撤单请求
@aztdataclass(proto.CancelOrder, adj_time=dict(send_time="%Y%m%d-%H:%M:%S"))
class CancelOrder:
    client_ref: str = None
    sender_user: str = None
    account: str = None
    org_order_id: str = None
    send_time: datetime.datetime = None
