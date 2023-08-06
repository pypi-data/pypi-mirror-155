import datetime

from ..tools.azt_dataclass import aztdataclass
from .api_struct import PlaceOrder
from ..protobufs import Message_pb2 as proto


# 用户注册回复信息
@aztdataclass(proto.UserRegisterInfo)
class UserRegisterInfo:
    strategy_id: str = None
    account: str = None
    passwd: str = None
    acc_status: int = None


# 注册回复信息
@aztdataclass(proto.RegisterAck)
class RegisterAck:
    registe_info: UserRegisterInfo = None
    regist_code: int = None


# 登录信息
@aztdataclass(proto.LoginInfo, adj_time=dict(exchange_time="%Y%m%d%H%M%S"))
class LoginInfo:
    account: str = None
    trading_day: str = None
    exchange_name: str = None
    exchange_time: datetime.datetime = None


@aztdataclass(proto.LoginAck)
class LoginAck:
    login_info: LoginInfo = None
    ret_code: int = None


# 账户资产信息
@aztdataclass(proto.AccMargin,
              amount_dec="amount_decimal_place",
              adj_amount=["total_amount", "available_amount", "deposit", "open_balance", "trade_frozen_margin",
                          "position_market_amount", "total_buy_amount", "total_buy_fee", "total_sell_amount",
                          "total_sell_fee"],
              )
class AccMargin:
    account: str = None
    total_amount: float = None
    available_amount: float = None
    deposit: float = None
    open_balance: float = None
    trade_frozen_margin: float = None
    position_market_amount: float = None
    total_buy_amount: float = None
    total_buy_fee: float = None
    total_sell_amount: float = None
    total_sell_fee: float = None
    # update_time: datetime.datetime = None


# 账户入金信息
@aztdataclass(proto.AccDepositAck)
class AccDepositAck:
    acc_margin: AccMargin = None
    error_code: int = None


@aztdataclass(proto.OrdStatusMsg, price_dec="price_decimal_place",
              adj_price=["traded_amount", "total_fee", "frozen_margin", "frozen_price"],
              adj_time=dict(report_time="%Y%m%d-%H:%M:%S"))
class OrdStatusMsg:
    order_status: int = None
    traded_qty: int = None
    traded_amount: float = None
    total_fee: float = None
    frozen_margin: float = None
    frozen_price: float = None
    reject_reason: int = None
    # reject_reason_detail: bytes = None
    report_time: datetime.datetime = None


@aztdataclass(proto.OrdReport)
class OrdReport:
    place_order: PlaceOrder = None
    status_msg: OrdStatusMsg = None


# 委托查询回复信息
@aztdataclass(proto.QueryOrdersAck, adj_repeat=["order_reports"])
class QueryOrdersAck:
    order_reports: [OrdReport] = None


# 成交回报信息
@aztdataclass(proto.TradeReport, price_dec="price_decimal_place", adj_price=["traded_price", "fee"],
              adj_time=dict(transact_time="%Y%m%d-%H:%M:%S"))
class TradeReport:
    order_id: str = None
    client_ref: str = None
    account: str = None
    market: str = None
    code: str = None
    traded_id: str = None
    traded_index: int = None
    exec_type: int = None
    traded_qty: int = None
    traded_price: float = None
    fee: float = None
    transact_time: datetime.datetime = None


# 交易明细查询回复信息
@aztdataclass(proto.QueryTradesAck, adj_repeat=["trade_reports"])
class QueryTradesAck:
    trade_reports: [TradeReport] = None


# 持仓信息
@aztdataclass(proto.StokPosition, price_dec="price_decimal_place", adj_price=["open_avg_price"])
class StockPosition:
    account: str = None
    market: str = None
    code: str = None
    total_qty: int = None
    today_qty: int = None
    open_avg_price: float = None
    surplus_close_qty: int = None
    frozen_qty: int = None
    # update_time: datetime.datetime = None

# 持仓查询回复信息
@aztdataclass(proto.QueryPositionsAck, adj_repeat=["positions"])
class QueryPositionsAck:
    positions: [StockPosition] = None


# 撤单拒绝回报
@aztdataclass(proto.CancelOrderReject, adj_time=dict(report_time="%Y%m%d%H%M%S"))
class CancelOrderReject:
    client_ref: str = None
    org_order_id: str = None
    reject_reason: int = None
    # reject_reason_detail: bytes = None  # todo 为什么是bytes？
    report_time: datetime.datetime = None
