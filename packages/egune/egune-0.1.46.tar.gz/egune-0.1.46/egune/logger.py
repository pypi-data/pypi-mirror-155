import logging
import time
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.formatter import LogstashFormatter
from egune.interfaces import ActorMessage, ActorResponse, Command, Interface, UserMessage
from typing import Callable, Dict, Any, List
import traceback


logger = logging.getLogger('')


def init_logger(config):
    global logger
    logger = logging.getLogger(config["name"])
    logger.setLevel(logging.INFO)
    logstash_formatter = LogstashFormatter(message_type=f"egune-{config['name']}")
    logstash_handler = AsynchronousLogstashHandler(config["host"], config["port"], None)
    logstash_handler.setFormatter(logstash_formatter)
    logger.addHandler(logstash_handler)
    logger.info(f"Started {config['name']}", extra={
        "log_event": "system started"
    })


def get_user_id(a):
    if "user_id" in a:
        return a["user_id"]
    else:
        return "unknown"


def log_request(request_name):
    def ultra_wrapped(func):
        def wrapped(self, data):
            s = time.time()
            try:
                input_str = str(data)
                result = func(self, data)
                logger.info("Processed", extra={
                    "log_event": request_name,
                    "user_id": get_user_id(data),
                    "process_input": str(data),
                    "process_output": str(result),
                    "time": time.time() - s
                })
                return result
            except Exception as e:
                logger.error("Failed", extra={
                    "log_event": request_name + ":Failed",
                    "user_id": get_user_id(data),
                    "process_input": str(data),
                    "process_output": traceback.format_exc(),
                    "time": time.time() - s
                })
                return e
        return wrapped
    return ultra_wrapped


def log(extra):
    logger.info("custom", extra=extra)
