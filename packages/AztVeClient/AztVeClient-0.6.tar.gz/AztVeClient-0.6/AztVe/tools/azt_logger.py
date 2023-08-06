import logging
import colorlog

_log_colors_config = {
    'DEBUG': 'green',
    # 'INFO': 'black',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}


class _AztLog:
    def __init__(self, filename=None, level=logging.INFO):
        self.filename = filename
        # formatter = logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S")

        self._logger = logging.getLogger(name="AztVe")
        self.formatter_filehdlr = logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S")
        self.formatter_streamhdlr = colorlog.ColoredFormatter("%(log_color)s[%(asctime)s] %(message)s",
                                                              "%Y-%m-%d %H:%M:%S",
                                                              log_colors=_log_colors_config)

        if filename:
            self.handle_ = logging.FileHandler(filename, encoding="utf-8", mode="a")
            self.handle_.setFormatter(self.formatter_filehdlr)
        else:
            self.handle_ = logging.StreamHandler()
            self.handle_.setFormatter(self.formatter_streamhdlr)

        self._logger.addHandler(self.handle_)
        self._logger.setLevel(level)

    def set_log2file(self, filename):
        if not self.filename or filename != self.filename:
            self._logger.removeHandler(self.handle_)
            self.handle_ = logging.FileHandler(filename, encoding="utf-8", mode="a")
            self.handle_.setFormatter(self.formatter_filehdlr)
            self._logger.addHandler(self.handle_)
            self.filename = filename

    def set_log2stream(self):
        if self.filename is not None:
            self._logger.removeHandler(self.handle_)
            self.handle_ = logging.StreamHandler()
            self.handle_.setFormatter(self.formatter_streamhdlr)
            self._logger.addHandler(self.handle_)
            self.filename = None

    def log_debug(self):
        self._logger.setLevel(logging.DEBUG)

    def log_info(self):
        self._logger.setLevel(logging.INFO)

    def log_warning(self):
        self._logger.setLevel(logging.WARNING)

    def log_error(self):
        self._logger.setLevel(logging.ERROR)

    def debug(self, *msgs):
        msgs = [str(msg) for msg in msgs]
        self._logger.debug("[测试] " + " ".join(msgs))

    def log(self, *msgs):
        msgs = [str(msg) for msg in msgs]
        self._logger.info(" ".join(msgs))

    def warning(self, *msgs):
        msgs = [str(msg) for msg in msgs]
        self._logger.warning("[警告] " + " ".join(msgs))

    def error(self, *msgs):
        msgs = [str(msg) for msg in msgs]
        self._logger.error("[错误] " + " ".join(msgs))


_logger = _AztLog()


# 日志设置函数
def init_azt_log(log_file=None, **kwargs):
    if log_file is not None:
        # azt_logger.log("已设置日志输出：", log_file)
        _logger.set_log2file(log_file)
    pass
    # 设置日志级别
    if kwargs.get("log_debug", False):
        _logger.log_debug()
    if kwargs.get("log_info", False):
        _logger.log_info()
    if kwargs.get("log_warning", False):
        _logger.log_warning()
    if kwargs.get("log_error", False):
        _logger.log_error()


# 日志函数
def debug(*msgs):
    _logger.debug(*msgs)


def log(*msgs):
    _logger.log(*msgs)


def warning(*msgs):
    _logger.warning(*msgs)


def error(*msgs):
    _logger.error(*msgs)