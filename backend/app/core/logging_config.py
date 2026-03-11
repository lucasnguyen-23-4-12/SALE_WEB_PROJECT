import json
import logging
import logging.config
import time
from contextvars import ContextVar
from datetime import datetime, timezone


request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)


class RequestContextFilter(logging.Filter):
    def __init__(self, service_name: str) -> None:
        super().__init__()
        self._service_name = service_name

    def filter(self, record: logging.LogRecord) -> bool:
        record.service = self._service_name
        record.request_id = request_id_ctx.get()
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat()
        payload: dict[str, object] = {
            "ts": ts,
            "level": record.levelname,
            "logger": record.name,
            "service": getattr(record, "service", None),
            "request_id": getattr(record, "request_id", None),
            "msg": record.getMessage(),
        }

        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)

        for key, value in record.__dict__.items():
            if key in {
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
                "service",
                "request_id",
            }:
                continue
            if key.startswith("_"):
                continue
            payload.setdefault(key, value)

        return json.dumps(payload, ensure_ascii=False, default=str)


def configure_json_logging(*, service_name: str = "backend") -> None:
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "request_context": {
                "()": RequestContextFilter,
                "service_name": service_name,
            }
        },
        "formatters": {
            "json": {
                "()": JsonFormatter,
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "json",
                "filters": ["request_context"],
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
        "loggers": {
            # Reduce duplicate access logs; app logs requests via middleware.
            "uvicorn.access": {"level": "WARNING", "propagate": True},
            # Ensure SQLAlchemy echo logs use JSON formatting too.
            "sqlalchemy.engine.Engine": {"level": "INFO", "handlers": ["console"], "propagate": False},
            "sqlalchemy.engine": {"level": "INFO", "handlers": ["console"], "propagate": False},
            "sqlalchemy.pool": {"level": "WARNING", "handlers": ["console"], "propagate": False},
            # Reduce noise from http client used in tests.
            "httpx": {"level": "WARNING", "propagate": True},
        },
    }

    logging.config.dictConfig(config)
