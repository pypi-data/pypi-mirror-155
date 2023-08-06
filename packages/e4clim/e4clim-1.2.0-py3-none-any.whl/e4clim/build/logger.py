import logging
from pathlib import Path
import sys
import typing as tp
from warnings import warn
from e4clim.application import Application
from e4clim.config import Config
import e4clim.typing as e4tp
from e4clim.utils import tools


#: Log depth for currentframe overriding.
DEPTH = 4

#: Override currentframe function because log call transmitted through
# and additional function call by `container.info` member.
logging.currentframe = lambda: sys._getframe(DEPTH)


class BuilderLoggerMixin:
    """Logger building mixin."""

    #: Configuration.
    _cfg: tp.Optional[Config]

    _product: Application

    @property
    def cfg(self) -> tp.Optional[Config]:
        return self._cfg

    @property
    def product(self) -> Application:
        return self._product

    def build_logger(self) -> None:
        """Buid logger.

        :raises AssertionError: if :py:attr:`cfg` attribute is `None`.
        """
        assert self.cfg is not None, '"cfg" attribute required'

        self.product.med._log = logging.getLogger(
            str(self.cfg['project_name']))

        _init_logger(self.product.med.log, self.cfg.get('log'))


def _init_logger(log: logging.Logger, cfg: e4tp.CfgType) -> None:
    """Initialize logger.

    :param log: Logger.
    :param cfg: Logger configuration.
    """
    # Prevent propagation (to Root logger)
    log.propagate = False

    _set_logger_level(log, cfg)

    hdlr = _create_logging_stream_handler(cfg)

    _add_logging_formatter_to_stream_handler(hdlr, log, cfg)

    _add_logging_handler_where_needed(hdlr, log, cfg)

    # logging.setLogRecordFactory(record_factory)


def _set_logger_level(log: logging.Logger, cfg: e4tp.CfgType,
                      default_level: str = 'INFO') -> None:
    """Set logger level and return it.

    :param log: Logger.
    :param cfg: Logger configuration.
    :param default_level: Default level.
    """
    if cfg is None:
        level = default_level
    else:
        level = tools.get_required_str_entry(cfg, 'level', default_level)

    log.setLevel(level)


def _add_logging_handler_where_needed(
        hdlr: logging.Handler, log: logging.Logger, cfg: e4tp.CfgType) -> None:
    """Add logging handler where needed.

    :param hdlr: Logging handler.
    :param log: Logger.
    :param cfg: Logger configuration.
    """
    _add_handler_to_root_logger(hdlr, log)
    _add_handler_to_warning_logger(hdlr, cfg)
    _add_handler_to_matplotlib_logger(hdlr)


def _add_handler_to_root_logger(
        hdlr: logging.Handler, log: logging.Logger) -> None:
    """Add handler to root logger if needed.

    :param hdlr: Logging handler.
    :param log: Logger.
    """
    if not log.hasHandlers():
        log.addHandler(hdlr)


def _add_handler_to_warning_logger(
        hdlr: logging.Handler, cfg: e4tp.CfgType,
        default_capture_warnings: bool = True) -> None:
    """Add handler to warning logger if needed.

    :param hdlr: Logging handler.
    :param cfg: Logger configuration.
    :param default_capture_warnings: Default flag for capturing warnings.
    """
    if cfg is None:
        capture_warnings = default_capture_warnings
    else:
        capture_warnings = tools.get_required_bool_entry(
            cfg, 'capture_warnings', default_capture_warnings)

    if capture_warnings:
        logging.captureWarnings(capture_warnings)
        warn_log = logging.getLogger('py.warnings')
        if not warn_log.hasHandlers():
            warn_log.addHandler(hdlr)


def _add_handler_to_matplotlib_logger(hdlr: logging.Handler) -> None:
    """Add handler to matplotlib logger if needed.

    :param hdlr: Logging handler.
    """
    mpl_log = logging.getLogger('matplotlib')
    if not mpl_log.hasHandlers():
        mpl_log.addHandler(hdlr)


def _create_logging_stream_handler(cfg: e4tp.CfgType) -> logging.Handler:
    """Create logging stream handler.

    :param cfg: Logger configuration.

    :returns: Stream handler.
    """
    log_filepath = tools.get_str_entry(
        cfg, 'filepath') if cfg is not None else None

    if log_filepath is None:
        return logging.StreamHandler()
    else:
        # If log_filepath given, log to file instead of stream
        log_filepath_safe = Path(*tools.ensure_collection(log_filepath, list))
        msg = ('Setting loggging to {}. '
               'Open it for further information'.format(log_filepath_safe))
        warn(msg)
        # Make sure that log-file directory exists
        Path.mkdir(log_filepath_safe.parent, parents=True, exist_ok=True)
        return logging.FileHandler(log_filepath_safe, mode='a')


def _add_logging_formatter_to_stream_handler(
        hdlr: logging.Handler, log: logging.Logger, cfg: e4tp.CfgType) -> None:
    """Add logging formatter to stream handler.

    :param hdlr: Stream handler.
    :param log: Logger.
    :param cfg: Logger configuration.
    """
    log_fmt = _get_logging_formatter_string(cfg)

    formatter = logging.Formatter(log_fmt)

    hdlr.setFormatter(formatter)

    hdlr.setLevel(log.getEffectiveLevel())


def _get_logging_formatter_string(cfg: e4tp.CfgType) -> str:
    """Get logging formater string.

    :param cfg: Logger configuration.

    :returns: Logging formatter string.
    """
    default_log_fmt = ('%(asctime)s/%(name)s/%(module)s.%(funcName)s:'
                       '%(lineno)d/%(levelname)s: %(message)s')
    if cfg is None:
        log_fmt_safe = default_log_fmt
    else:
        log_fmt = tools.get_str_entry(cfg, 'log_fmt')
        if log_fmt is None:
            log_fmt_safe = default_log_fmt
        else:
            log_fmt_safe = log_fmt

    return log_fmt_safe
