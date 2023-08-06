import logging
import time
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.formatter import LogstashFormatter
from egune.interfaces import ActorMessage, ActorResponse, Command, Interface, UserMessage
from typing import Callable, Dict, Any, List
import traceback
import json


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


def log_request(request_name, input_prep, output_prep):
    def ultra_wrapped(func):
        def wrapped(data):
            s = time.time()
            try:
                result = output_prep(func(input_prep(data)))
                logger.info("Processed", extra={
                    "log_event": request_name,
                    "process_input": data,
                    "process_output": result,
                    "time": time.time() - s
                })
                return result
            except Exception as e:
                logger.error("Failed", extra={
                    "log_event": request_name + ":Failed",
                    "process_input": data,
                    "process_output": traceback.format_exc(),
                    "time": time.time() - s
                })
                return e
        return wrapped
    return ultra_wrapped


def log(extra):
    logger.info("custom", extra=extra)
