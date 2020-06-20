import logging
import sys
import structlog
import logging.config


def create_logger(ARGS, level="INFO", **kwargs):

    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    # will default to utc time, can pass utc=False to use local time
    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
    pre_chain = [
        # adding the log level and timestamp to each log message
        structlog.stdlib.add_log_level,
        timestamper
    ]

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "colored": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.dev.ConsoleRenderer(colors=True),
                    "foreign_pre_chain": pre_chain,
                },
            },
            "handlers": {
                "default": {"level": log_levels[ARGS.log_level], "class": "logging.StreamHandler", "formatter": "colored"}
            },
            "loggers": {"": {"handlers": ["default"], "level": log_levels[ARGS.log_level], "propagate": True,},},
        }
    )

    processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        timestamper,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
    )      
    