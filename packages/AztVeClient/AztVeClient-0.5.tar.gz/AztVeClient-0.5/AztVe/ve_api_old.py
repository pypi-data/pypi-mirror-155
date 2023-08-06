import datetime
from .vexchange_api import *
from .structs import api_struct
from .tools import azt_errors

_AllowOrderTimeSHSE_SZSE = (
    datetime.time(9, 30, 0), datetime.time(11, 30, 0),
    datetime.time(13, 0), datetime.time(20, 0),
)


class AztVeApiOld(CVexchangeTraderApi):

    # ------ RegisterReq ------
    def RegisterReq(self, req: api_struct.RegisterReq, sync=False, timeout=3):
        super(AztVeApiOld, self).RegisterReq(req.__py2proto__())
        if sync:
            spi_name = "onRegisterReq"
            self._queue_subscribe(spi_name)
            ret = self._queue_get(spi_name, timeout=timeout)
            self._queue_unsubscribe(spi_name)
            return ret

    # ------ LoginReq ------
    def UserLoginReq(self, req: api_struct.LoginReq, sync=False, timeout=3):
        self._sender_user = req.account
        # self._logined = True
        super(AztVeApiOld, self).UserLoginReq(req.__py2proto__())
        if sync:
            spi_name = "onUserLoginReq"
            self._queue_subscribe(spi_name)
            ret = self._queue_get(spi_name, timeout=timeout)
            self._queue_unsubscribe(spi_name)
            return ret

    # ------ LogoutReq ------
    def UserLogoutReq(self, req: api_struct.LogoutReq):
        if not self._logined:
            self._close()
            raise azt_errors.NotLoginedError
        super(AztVeApiOld, self).UserLogoutReq(req.__py2proto__())
        self._close()
        azt_logger.log("已退出登录，欢迎下次使用！")

    # ------ UserInfoQryReq ------
    def UserInfoQryReq(self, req: api_struct.UserInfoQryReq, sync=False, timeout=3):
        super(AztVeApiOld, self).UserInfoQryReq(req.__py2proto__())
        if sync:
            spi_name = "onUserInfoQryReq"
            self._queue_subscribe(spi_name)
            ret = self._queue_get(spi_name, timeout=timeout)
            self._queue_unsubscribe(spi_name)
            return ret

    # ------ AccDepositReq ------
    def AccDepositReq(self, req: api_struct.AccDepositReq, sync=False, timeout=3):
        if not self._logined:
            self._close()
            raise azt_errors.NotLoginedError
        req.client_ref = self._client_ref
        req.sender_user = self._sender_user
        req.send_time = datetime.datetime.now()
        super(AztVeApiOld, self).AccDepositReq(req.__py2proto__())
        if sync:
            spi_name = "onAccDepositReq"
            self._queue_subscribe(spi_name)
            ret = self._queue_get(spi_name, timeout=timeout)
            self._queue_unsubscribe(spi_name)
            return ret

    # ------ TradingAccQryReq ------
    def TradingAccQryReq(self, req: api_struct.TradingAccQryReq, sync=False, timeout=3):
        if not self._logined:
            self._close()
            raise azt_errors.NotLoginedError
        super(AztVeApiOld, self).TradingAccQryReq(req.__py2proto__())
        if sync:
            spi_name = "onTradingAccQryReq"
            self._queue_subscribe(spi_name)
            ret = self._queue_get(spi_name, timeout=timeout)
            self._queue_unsubscribe(spi_name)
            return ret

    # ------ QueryOrdersReq ------
    def QueryOrdersReq(self, req: api_struct.QueryOrdersReq, sync=False, timeout=3):
        if not self._logined:
            self._close()
            raise azt_errors.NotLoginedError
        req.client_ref = self._client_ref
        super(AztVeApiOld, self).QueryOrdersReq(req.__py2proto__())
        if sync:
            spi_name = "onQueryOrdersReq"
            self._queue_subscribe(spi_name)
            ret = self._queue_get(spi_name, timeout=timeout)
            self._queue_unsubscribe(spi_name)
            return ret

    # ------ QueryTradesReq ------
    def QueryTradesReq(self, req: api_struct.QueryTradesReq, sync=False, timeout=3):
        if not self._logined:
            self._close()
            raise azt_errors.NotLoginedError
        super(AztVeApiOld, self).QueryTradesReq(req.__py2proto__())
        if sync:
            spi_name = "onQueryTradesReq"
            self._queue_subscribe(spi_name)
            ret = self._queue_get(spi_name, timeout=timeout)
            self._queue_unsubscribe(spi_name)
            return ret

    # ------ QueryPositionsReq ------
    def QueryPositionsReq(self, req: api_struct.QueryPositionsReq, sync=False, timeout=3):
        if not self._logined:
            self._close()
            raise azt_errors.NotLoginedError
        super(AztVeApiOld, self).QueryPositionsReq(req.__py2proto__())
        if sync:
            spi_name = "onQueryPositionsReq"
            self._queue_subscribe(spi_name)
            ret = self._queue_get(spi_name, timeout=timeout)
            self._queue_unsubscribe(spi_name)
            return ret

    # ------ QueryHistoryOrdersReq ------
    def QueryHistoryOrdersReq(self, req: api_struct.QueryHistoryOrdersReq, sync=False, timeout=3):
        if not self._logined:
            self._close()
            raise azt_errors.NotLoginedError
        super(AztVeApiOld, self).QueryHistoryOrdersReq(req.__py2proto__())
        if sync:
            spi_name = "onQueryHistoryOrdersReq"
            self._queue_subscribe(spi_name)
            ret = self._queue_get(spi_name, timeout=timeout)
            self._queue_unsubscribe(spi_name)
            return ret

    # ------ QueryHistoryTradesReq ------
    def QueryHistoryTradesReq(self, req: api_struct.QueryHistoryTradesReq, sync=False, timeout=3):
        if not self._logined:
            self._close()
            raise azt_errors.NotLoginedError
        super(AztVeApiOld, self).QueryHistoryTradesReq(req.__py2proto__())
        if sync:
            spi_name = "onQueryHistoryTradesReq"
            self._queue_subscribe(spi_name)
            ret = self._queue_get(spi_name, timeout=timeout)
            self._queue_unsubscribe(spi_name)
            return ret

    # ------ PlaceOrder ------
    def PlaceOrder(self, req: api_struct.PlaceOrder):
        if not self._logined:
            self._close()
            raise azt_errors.NotLoginedError
        req.client_ref = self._client_ref
        req.sender_user = self._sender_user
        now = datetime.datetime.now()
        now_time = now.time()
        if _AllowOrderTimeSHSE_SZSE[0] <= now_time <= _AllowOrderTimeSHSE_SZSE[1] or \
                _AllowOrderTimeSHSE_SZSE[2] <= now_time <= _AllowOrderTimeSHSE_SZSE[3]:
            req.send_time = now
            super(AztVeApiOld, self).PlaceOrder(req.__py2proto__())
        else:
            raise azt_errors.NonTradingTimeError

    # ------ CancelOrder ------
    def CancelOrder(self, req: api_struct.CancelOrder):
        if not self._logined:
            self._close()
            raise azt_errors.NotLoginedError
        req.client_ref = self._client_ref
        req.sender_user = self._sender_user
        req.send_time = datetime.datetime.now()
        super(AztVeApiOld, self).CancelOrder(req.__py2proto__())
