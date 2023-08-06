from .ve_api_old import *


class AztVeSpi:
    api = None

    def onRegisterAccount(self, msg):
        pass

    def onLogin(self, msg):
        pass

    def onQueryAccountInfo(self, msg):
        pass

    def onDepositAsset(self, msg):
        pass

    def onQueryAsset(self, msg):
        pass

    def onQueryOrders(self, msg):
        pass

    def onQueryTrades(self, msg):
        pass

    def onQueryPositions(self, msg):
        pass

    def onQueryHistoryOrders(self, msg):
        pass

    def onQueryHistoryTrades(self, msg):
        pass

    def onOrderReport(self, msg):
        pass

    def onTradeReport(self, msg):
        pass

    def onCancelOrderReject(self, msg):
        pass


class _SpiApdapter(CVexchangeTraderSpi):
    __new_spi = AztVeSpi()

    def register_new_spi(self, new_spi):
        self.__new_spi = new_spi

    def onRegisterReq(self, msg):
        self.__new_spi.onRegisterAccount(msg)

    def onUserLoginReq(self, msg):
        self.__new_spi.onLogin(msg)

    def onUserInfoQryReq(self, msg):
        self.__new_spi.onQueryAccountInfo(msg)

    def onAccDepositReq(self, msg):
        self.__new_spi.onDepositAsset(msg)

    def onTradingAccQryReq(self, msg):
        self.__new_spi.onQueryAsset(msg)

    def onQueryOrdersReq(self, msg):
        self.__new_spi.onQueryOrders(msg)

    def onQueryTradesReq(self, msg):
        self.__new_spi.onQueryTrades(msg)

    def onQueryPositionsReq(self, msg):
        self.__new_spi.onQueryPositions(msg)

    def onQueryHistoryOrdersReq(self, msg):
        self.__new_spi.onQueryHistoryOrders(msg)

    def onQueryHistoryTradesReq(self, msg):
        self.__new_spi.onQueryHistoryTrades(msg)

    def onOrderReport(self, msg):
        self.__new_spi.onOrderReport(msg)

    def onTradeReport(self, msg):
        self.__new_spi.onTradeReport(msg)

    def onCancelOrderReject(self, msg):
        self.__new_spi.onCancelOrderReject(msg)


class AztVeApi:

    def __init__(self):
        self.__api = AztVeApiOld()
        # self.__api.RegisterSpi(_SpiApdapter)
        self.__account = None

    # 初始化
    def Init(self, server_addr: str, spi = None, log_file: str = None, **kwargs):
        _spi = _SpiApdapter()
        if spi is not None:
            if spi.__class__ is type:
                spi = spi()
            _spi.register_new_spi(spi)

        self.__api.Init(server_addr, _spi, log_file, **kwargs)

    # # 注册Spi
    # def RegisterSpi(self, spi):
    #     if spi.__class__ is type:
    #         spi = spi()
    #     if hasattr(self.__api.spi, "register_new_spi"):
    #         spi.api = self
    #         self.__api.spi.register_new_spi(spi)
    #     else:
    #         self.__api.RegisterSpi(spi)

    # 注册账户
    def RegisterAccount(self, strategy_id: str, strategy_check_code: str, sync: bool = False, timeout: int = None):
        register_req = api_struct.RegisterReq(
            strategy_id=strategy_id,
            strategy_check_code=strategy_check_code,
        )
        return self.__api.RegisterReq(register_req, sync, timeout)

    # #
    # def log(self, *msgs):
    #     self.__api.log(*msgs)

    # 登录
    def Login(self, account: str, passwd: str, sync: bool = False, timeout: int = None):
        self.__account = account
        login_req = api_struct.LoginReq(account=account, passwd=passwd)
        return self.__api.UserLoginReq(login_req, sync, timeout)

    # 登出
    def Logout(self):
        logout_req = api_struct.LogoutReq(account=self.__account)
        self.__api.UserLogoutReq(logout_req)

    # 查询账户信息
    def QueryAccountInfo(self, strategy_id: str = None, strategy_check_code: str = None, account: str = None,
                         passwd: str = None, sync: bool = False, timeout: int = None):
        if not strategy_id and not strategy_check_code:
            if not account and not passwd:
                raise azt_errors.ArgsError("参数必须填写strategy_id和strategy_check_code（查询账户所有信息）或者account和passwd（查询账户状态）！")
            account_info_req = api_struct.UserInfoQryReq(account=account, passwd=passwd)
        else:
            account_info_req = api_struct.UserInfoQryReq(
                strategy_id=strategy_id,
                strategy_check_code=strategy_check_code
            )
        return self.__api.UserInfoQryReq(account_info_req, sync, timeout)

    # 账户入金
    def DepositAsset(self, amount: float, sync: bool = False, timeout: int = None):
        accdeposit_req = api_struct.AccDepositReq(account=self.__account, amount=amount)
        return self.__api.AccDepositReq(accdeposit_req, sync, timeout)

    # 查询账户资产信息
    def QueryAsset(self, sync: bool = False, timeout: int = None):
        trade_req = api_struct.TradingAccQryReq(account=self.__account)
        return self.__api.TradingAccQryReq(trade_req, sync, timeout)

    # 查询订单信息
    def QueryOrders(self, market: str = None, code: str = None, order_id: str = None, unfinished: bool = False,
                    sync: bool = False, timeout: int = None):
        order_req = api_struct.QueryOrdersReq(account=self.__account, market=market, code=code, order_id=order_id,
                                              unfinished=unfinished)
        return self.__api.QueryOrdersReq(order_req, sync, timeout)

    # 查询交易信息
    def QueryTrades(self, market: str = None, code: str = None, order_id: str = None, trade_id: str = None,
                    sync: bool = False, timeout: int = None):
        trade_req = api_struct.QueryTradesReq(account=self.__account, market=market, code=code, order_id=order_id,
                                              trade_id=trade_id)
        return self.__api.QueryTradesReq(trade_req, sync, timeout)

    # 查询持仓信息
    def QueryPositions(self, market: str = None, code: str = None, sync: bool = False, timeout: int = None):
        position_req = api_struct.QueryPositionsReq(account=self.__account, market=market, code=code)
        return self.__api.QueryPositionsReq(position_req, sync, timeout)

    # 查询历史委托信息
    def QueryHistoryOrders(self, market: str = None, code: str = None, start_time: datetime.datetime = None,
                           end_time: datetime.datetime = None, sync: bool = False, timeout: int = None):
        historyorders_req = api_struct.QueryHistoryOrdersReq(account=self.__account, market=market, code=code,
                                                             start_time=start_time, end_time=end_time)
        return self.__api.QueryHistoryOrdersReq(historyorders_req, sync, timeout)

    # 查询历史交易信息
    def QueryHistoryTrades(self, market: str = None, code: str = None, start_time: datetime.datetime = None,
                           end_time: datetime.datetime = None, sync: bool = False, timeout: int = None):
        historytrades_req = api_struct.QueryHistoryTradesReq(account=self.__account, market=market, code=code,
                                                             start_time=start_time, end_time=end_time)
        return self.__api.QueryHistoryTradesReq(historytrades_req, sync, timeout)

    def InsertOrder(self, market: str, code: str, order_type: int, order_side: int, effect: int,
                    order_price: float, order_qty: int, discretion_price: float):
        order_req = api_struct.PlaceOrder(
            account=self.__account,
            market=market,
            code=code,
            order_type=order_type,
            business_type=EnumProto.KBusinessType_NORMAL,
            order_side=order_side,
            effect=effect,
            order_price=order_price,
            order_qty=order_qty,
            discretion_price=discretion_price
        )
        self.__api.PlaceOrder(order_req)

    # 买入委托
    def Buy(self, market: str, code: str,
            order_qty: int = 100,  # 默认买入1手(100股)
            order_type: int = EnumProto.KOrderType_Market,  # 默认市价委托
            effect: int = EnumProto.KPositionEffect_Open,  # 默认多仓委托,股票委托不用关注
            order_price: float = None,  # 委托限价,适用于限价单,保留两位小数
            discretion_price: float = None  # 市价转限价后委托限价,适用于市价转限价委托,保留两位小数
            ):
        self.InsertOrder(market, code, order_type, EnumProto.KOrderDirection_Buy, effect, order_price, order_qty,
                         discretion_price)

    # 卖出委托
    def Sell(self, market: str, code: str,
             order_qty: int = 100,  # 默认卖出1手(100股)
             order_type: int = EnumProto.KOrderType_Market,  # 默认市价委托
             effect: int = EnumProto.KPositionEffect_Close,  # 默认空仓委托,股票委托不用关注
             order_price: float = None,  # 委托限价,适用于限价单,保留两位小数
             discretion_price: float = None  # 市价转限价后委托限价,适用于市价转限价委托,保留两位小数
             ):
        self.InsertOrder(market, code, order_type, EnumProto.KOrderDirection_Buy, effect, order_price, order_qty,
                         discretion_price)

    # 撤单委托
    def Cancel(self, order_id: str):
        order_req = api_struct.CancelOrder(account=self.__account, org_order_id=order_id)
        self.__api.CancelOrder(order_req)

    def Join(self, timeout: int = None):
        self.__api.Join(timeout=timeout)
