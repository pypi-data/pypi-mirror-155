#!/bin/env python
# -*- coding: UTF-8 -*-
import queue, threading, zmq, uuid
from abc import ABC, ABCMeta
from .protobufs import MsgType_pb2 as MsgTypeProto, Message_pb2 as MsgProto, EnumType_pb2 as EnumProto
from .protobufs import UnitedMessage_pb2 as UnitMsgProto
from .structs import spi_struct
from .tools import azt_logger


class CVexchangeTraderSpi(ABC):
    api = None

    def onRegisterReq(self, msg):
        pass

    def onUserLoginReq(self, msg):
        pass

    def onUserInfoQryReq(self, msg):
        pass

    def onAccDepositReq(self, msg):
        pass

    def onTradingAccQryReq(self, msg):
        pass

    def onQueryOrdersReq(self, msg):
        pass

    def onQueryTradesReq(self, msg):
        pass

    def onQueryPositionsReq(self, msg):
        pass

    def onQueryHistoryOrdersReq(self, msg):
        pass

    def onQueryHistoryTradesReq(self, msg):
        pass

    def onOrderReport(self, msg):
        pass

    def onTradeReport(self, msg):
        pass

    def onCancelOrderReject(self, msg):
        pass


class CVexchangeTraderApi:
    def __init__(self):
        # 服务器地址
        self._server_addr = None
        # 设置默认的spi
        self.spi = CVexchangeTraderSpi()
        # 设置zmq
        self.__context = zmq.Context()
        self.__socket = self.__context.socket(zmq.DEALER)
        # 设置线程
        self.__thread_id = threading.Thread(target=self.__report_recv)
        self.__thread_id.setDaemon(True)
        # 设置信号
        self._logined = False
        self.__closed = False
        # 同步管道
        self._queue_map = dict()
        # 设置client_ref标识
        self._client_ref = str(uuid.uuid4())
        # 设置策略ID
        self._sender_user = None
        # self._logger = AztLog(filename=logfile)

    # def log(self, *msgs):
    #     self._logger.log(*msgs)

    # def RegisterSpi(self, azt_spi):
    #     """
    #     注册spi
    #     :param azt_spi: 回调类,可以直接将类传入,也可以传入类实例
    #     """
    #     if azt_spi.__class__ is ABCMeta:
    #         azt_spi = azt_spi()
    #     self.spi = azt_spi
    #     self.spi.api = self

    def _queue_subscribe(self, spi_name):
        self._queue_map[spi_name] = queue.Queue()

    def _queue_get(self, spi_name, timeout=None):
        if spi_name in self._queue_map:
            try:
                return self._queue_map[spi_name].get(timeout=timeout)
            except queue.Empty:
                return None
        return None

    def _queue_unsubscribe(self, spi_name):
        if spi_name in self._queue_map:
            self._queue_map.pop(spi_name)

    def Init(self, server_addr: str, spi=None, log_file=None, **kwargs):
        # 设置日志
        if log_file is not None:
            # azt_logger.log("已设置日志输出：", log_file)
            azt_logger._logger.set_log2file(log_file)

        # 设置日志级别
        if kwargs.get("log_debug", False):
            azt_logger.log_debug()
        if kwargs.get("log_info", False):
            azt_logger.log_info()
        if kwargs.get("log_warning", False):
            azt_logger.log_warning()
        if kwargs.get("log_error", False):
            azt_logger.log_error()

        # 设置服务器地址
        if not server_addr.startswith("tcp"):
            server_addr = f"tcp://{server_addr}"
        self._server_addr = server_addr
        # 连接服务器
        self.__socket.connect(self._server_addr)

        # 设置spi
        if spi is not None:
            if spi.__class__ is ABCMeta:
                spi = spi()
            self.spi = spi
            self.spi.api = self

        azt_logger.log(f"已申请连接服务器 - {self._server_addr}")
        # 启动监听线程
        self.__thread_id.start()

    def _close(self):
        self.__closed = True
        # print("正在断开与服务器的连接...如长时间无反应请自行中止客户端！")
        # exit(1)
        # todo 当zmq无法找到服务器时,无法中止程序,exit太过暴力
        try:
            self.__socket.close()
            self.__context.destroy()
        except KeyboardInterrupt:
            exit(1)
        except Exception as e:
            raise e

    def __report_recv(self):  # 加__作为私有方法

        poller = zmq.Poller()
        poller.register(self.__socket, zmq.POLLIN)
        while True:
            try:
                events = poller.poll()  # poll模式是用于多个socket场景的,可以避免某个socket的接收阻塞问题,这里用不用都行
            except zmq.error.ZMQError as zmqerror:
                if self.__closed:
                    break
                raise zmqerror
            except Exception as e:
                raise e

            if self.__socket in dict(events):
                recv_msg = self.__socket.recv()
                unit_msg = UnitMsgProto.UnitedMessage()
                unit_msg.ParseFromString(recv_msg)
                self.__report_handel(unit_msg)

    def __report_handel(self, unit_msg):
        # print(f"收到消息：{ unit_msg.msg_type}-{unit_msg.msg_id}")
        if unit_msg.msg_type != MsgTypeProto.KMsgType_Exchange_Rsp:
            return
        "-----------"
        # trade_spi
        if unit_msg.msg_id == EnumProto.KVexchangeMsgID_RegisterAck:
            msg = MsgProto.RegisterAck()
            unit_msg.msg_body.Unpack(msg)
            azt_logger.debug(msg)
            cbmsg = spi_struct.RegisterAck.__proto2py__(msg)
            self.spi.onRegisterReq(cbmsg)
            if "onRegisterReq" in self._queue_map:
                self._queue_map["onRegisterReq"].put(cbmsg, block=False)

        elif unit_msg.msg_id == EnumProto.KVexchangeMsgID_LoginAck:
            self._logined = True
            msg = MsgProto.LoginAck()
            unit_msg.msg_body.Unpack(msg)
            azt_logger.debug(msg)
            cbmsg = spi_struct.LoginAck.__proto2py__(msg)
            self.spi.onUserLoginReq(cbmsg)
            if "onUserLoginReq" in self._queue_map:
                self._queue_map["onUserLoginReq"].put(cbmsg, block=False)

        elif unit_msg.msg_id == EnumProto.KVexchangeMsgID_UserInfoQryAck:
            msg = MsgProto.UserRegisterInfo()
            unit_msg.msg_body.Unpack(msg)
            azt_logger.debug(msg)
            cbmsg = spi_struct.UserRegisterInfo.__proto2py__(msg)
            self.spi.onUserInfoQryReq(cbmsg)
            if "onUserInfoQryReq" in self._queue_map:
                self._queue_map["onUserInfoQryReq"].put(cbmsg, block=False)

        elif unit_msg.msg_id == EnumProto.KTradeReqType_AccDepositAck:
            msg = MsgProto.AccDepositAck()
            unit_msg.msg_body.Unpack(msg)
            azt_logger.debug(msg)
            cbmsg = spi_struct.AccDepositAck.__proto2py__(msg)
            self.spi.onAccDepositReq(cbmsg)
            if "onAccDepositReq" in self._queue_map:
                self._queue_map["onAccDepositReq"].put(cbmsg, block=False)

        elif unit_msg.msg_id == EnumProto.KTradeReqType_TradingAccQryAck:
            msg = MsgProto.AccMargin()
            unit_msg.msg_body.Unpack(msg)
            azt_logger.debug(msg)
            cbmsg = spi_struct.AccMargin.__proto2py__(msg)
            self.spi.onTradingAccQryReq(cbmsg)
            if "onTradingAccQryReq" in self._queue_map:
                self._queue_map["onTradingAccQryReq"].put(cbmsg, block=False)

        elif unit_msg.msg_id == EnumProto.KQueryOrdersAck:
            msg = MsgProto.QueryOrdersAck()
            unit_msg.msg_body.Unpack(msg)
            azt_logger.debug(msg)
            cbmsg = spi_struct.QueryOrdersAck.__proto2py__(msg)
            self.spi.onQueryOrdersReq(cbmsg)
            if "onQueryOrdersReq" in self._queue_map:
                self._queue_map["onQueryOrdersReq"].put(cbmsg, block=False)

        elif unit_msg.msg_id == EnumProto.KQueryTradesAck:
            msg = MsgProto.QueryTradesAck()
            unit_msg.msg_body.Unpack(msg)
            azt_logger.debug(msg)
            cbmsg = spi_struct.QueryTradesAck.__proto2py__(msg)
            self.spi.onQueryTradesReq(cbmsg)
            if "onQueryTradesReq" in self._queue_map:
                self._queue_map["onQueryTradesReq"].put(cbmsg, block=False)

        elif unit_msg.msg_id == EnumProto.KQueryPositionsAck:
            msg = MsgProto.QueryPositionsAck()
            unit_msg.msg_body.Unpack(msg)
            azt_logger.debug(msg)
            cbmsg = spi_struct.QueryPositionsAck.__proto2py__(msg)
            self.spi.onQueryPositionsReq(cbmsg)
            if "onQueryPositionsReq" in self._queue_map:
                self._queue_map["onQueryPositionsReq"].put(cbmsg, block=False)

        elif unit_msg.msg_id == EnumProto.KQueryHistoryOrdersAck:
            msg = MsgProto.QueryTradesAck()
            unit_msg.msg_body.Unpack(msg)
            azt_logger.debug(msg)
            cbmsg = spi_struct.QueryTradesAck.__proto2py__(msg)
            self.spi.onQueryHistoryOrdersReq(cbmsg)
            if "onQueryHistoryOrdersReq" in self._queue_map:
                self._queue_map["onQueryHistoryOrdersReq"].put(cbmsg, block=False)

        elif unit_msg.msg_id == EnumProto.KQueryHistoryTradesAck:
            msg = MsgProto.QueryPositionsAck()
            unit_msg.msg_body.Unpack(msg)
            azt_logger.debug(msg)
            cbmsg = spi_struct.QueryPositionsAck.__proto2py__(msg)
            self.spi.onQueryHistoryTradesReq(cbmsg)
            if "onQueryHistoryTradesReq" in self._queue_map:
                self._queue_map["onQueryHistoryTradesReq"].put(cbmsg, block=False)

        # ----------------------------------------------------------
        elif unit_msg.msg_id == EnumProto.KTradeRspType_OrdStatusReport:
            msg = MsgProto.OrdReport()
            unit_msg.msg_body.Unpack(msg)
            azt_logger.debug(msg)
            self.spi.onOrderReport(spi_struct.OrdReport.__proto2py__(msg))

        elif unit_msg.msg_id == EnumProto.KTradeReqType_ExecReport:
            msg = MsgProto.TradeReport()
            unit_msg.msg_body.Unpack(msg)
            azt_logger.debug(msg)
            self.spi.onTradeReport(spi_struct.TradeReport.__proto2py__(msg))

        elif unit_msg.msg_id == EnumProto.KTradeReqType_RejectCancelReport:
            msg = MsgProto.CancelOrderReject()
            unit_msg.msg_body.Unpack(msg)
            azt_logger.debug(msg)
            self.spi.onCancelOrderReject(spi_struct.CancelOrderReject.__proto2py__(msg))
        else:
            azt_logger.warning("Unkown recv msg msg_id!")

    # ----------------------------------------------------------------------------------------
    def Join(self, timeout: int = None):
        self.__thread_id.join(timeout=timeout)

    # ------ RegisterReq ------
    def RegisterReq(self, req_msg: MsgProto.RegisterReq):
        unit_msg = UnitMsgProto.UnitedMessage()
        unit_msg.msg_type = MsgTypeProto.KMsgType_Exchange_Req
        unit_msg.msg_id = EnumProto.KVexchangeMsgID_RegisterReq
        unit_msg.msg_body.Pack(req_msg)

        self.__socket.send(unit_msg.SerializeToString())

    # ------ LoginReq ------
    def UserLoginReq(self, req_msg: MsgProto.LoginReq):
        unit_msg = UnitMsgProto.UnitedMessage()
        unit_msg.msg_type = MsgTypeProto.KMsgType_Exchange_Req
        unit_msg.msg_id = EnumProto.KVexchangeMsgID_LoginReq
        unit_msg.msg_body.Pack(req_msg)
        self.__socket.send(unit_msg.SerializeToString())

    # ------ LogoutReq ------
    def UserLogoutReq(self, req_msg: MsgProto.LogoutReq):
        unit_msg = UnitMsgProto.UnitedMessage()
        unit_msg.msg_type = MsgTypeProto.KMsgType_Exchange_Req
        unit_msg.msg_id = EnumProto.KVexchangeMsgID_LogoutReq
        unit_msg.msg_body.Pack(req_msg)

        self.__socket.send(unit_msg.SerializeToString())

    # ------ UserInfoQryReq ------
    def UserInfoQryReq(self, req_msg: MsgProto.UserInfoQryReq):
        unit_msg = UnitMsgProto.UnitedMessage()
        unit_msg.msg_type = MsgTypeProto.KMsgType_Exchange_Req
        unit_msg.msg_id = EnumProto.KVexchangeMsgID_UserInfoQryReq
        unit_msg.msg_body.Pack(req_msg)

        self.__socket.send(unit_msg.SerializeToString())

    # ------ AccDepositReq ------
    def AccDepositReq(self, req_msg: MsgProto.AccDepositReq):
        unit_msg = UnitMsgProto.UnitedMessage()
        unit_msg.msg_type = MsgTypeProto.KMsgType_Exchange_Req
        unit_msg.msg_id = EnumProto.KTradeReqType_AccDepositReq
        unit_msg.msg_body.Pack(req_msg)
        self.__socket.send(unit_msg.SerializeToString())

    # ------ TradingAccQryReq ------
    def TradingAccQryReq(self, req_msg: MsgProto.TradingAccQryReq):
        unit_msg = UnitMsgProto.UnitedMessage()
        unit_msg.msg_type = MsgTypeProto.KMsgType_Exchange_Req
        unit_msg.msg_id = EnumProto.KTradeReqType_TradingAccQryReq
        unit_msg.msg_body.Pack(req_msg)

        self.__socket.send(unit_msg.SerializeToString())

    # ------ QueryOrdersReq ------
    def QueryOrdersReq(self, req_msg: MsgProto.QueryOrdersReq):
        unit_msg = UnitMsgProto.UnitedMessage()
        unit_msg.msg_type = MsgTypeProto.KMsgType_Exchange_Req
        unit_msg.msg_id = EnumProto.KQueryOrdersReq
        unit_msg.msg_body.Pack(req_msg)

        self.__socket.send(unit_msg.SerializeToString())

    # ------ QueryTradesReq ------
    def QueryTradesReq(self, req_msg: MsgProto.QueryTradesReq):
        unit_msg = UnitMsgProto.UnitedMessage()
        unit_msg.msg_type = MsgTypeProto.KMsgType_Exchange_Req
        unit_msg.msg_id = EnumProto.KQueryTradesReq
        unit_msg.msg_body.Pack(req_msg)

        self.__socket.send(unit_msg.SerializeToString())

    # ------ QueryPositionsReq ------
    def QueryPositionsReq(self, req_msg: MsgProto.QueryPositionsReq):
        unit_msg = UnitMsgProto.UnitedMessage()
        unit_msg.msg_type = MsgTypeProto.KMsgType_Exchange_Req
        unit_msg.msg_id = EnumProto.KQueryPositionsReq
        unit_msg.msg_body.Pack(req_msg)

        self.__socket.send(unit_msg.SerializeToString())

    # ------ QueryHistoryOrdersReq ------

    def QueryHistoryOrdersReq(self, req_msg: MsgProto.QueryHistoryOrdersReq):
        unit_msg = UnitMsgProto.UnitedMessage()
        unit_msg.msg_type = MsgTypeProto.KMsgType_Exchange_Req
        unit_msg.msg_id = EnumProto.KQueryHistoryOrdersReq
        unit_msg.msg_body.Pack(req_msg)

        self.__socket.send(unit_msg.SerializeToString())

    # ------ QueryHistoryTradesReq ------
    def QueryHistoryTradesReq(self, req_msg: MsgProto.QueryHistoryTradesReq):
        unit_msg = UnitMsgProto.UnitedMessage()
        unit_msg.msg_type = MsgTypeProto.KMsgType_Exchange_Req
        unit_msg.msg_id = EnumProto.KQueryHistoryTradesReq
        unit_msg.msg_body.Pack(req_msg)

        self.__socket.send(unit_msg.SerializeToString())

    # ------ PlaceOrder ------
    def PlaceOrder(self, req_msg: MsgProto.PlaceOrder):
        unit_msg = UnitMsgProto.UnitedMessage()
        unit_msg.msg_type = MsgTypeProto.KMsgType_Exchange_Req
        unit_msg.msg_id = EnumProto.KTradeReqType_PlaceOrder
        unit_msg.msg_body.Pack(req_msg)

        self.__socket.send(unit_msg.SerializeToString())

    # ------ CancelOrder ------
    def CancelOrder(self, req_msg: MsgProto.CancelOrder):
        unit_msg = UnitMsgProto.UnitedMessage()
        unit_msg.msg_type = MsgTypeProto.KMsgType_Exchange_Req
        unit_msg.msg_id = EnumProto.KTradeReqType_CancelOrder
        unit_msg.msg_body.Pack(req_msg)

        self.__socket.send(unit_msg.SerializeToString())
