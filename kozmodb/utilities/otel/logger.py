import logging

from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs._internal.export import LogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource

from kozmodb.utilities.log import get_kozmodb_log_level


def setup_logger(resource: Resource, exporter: LogExporter) -> None:
    """
    Setup OpenTelemetry logging
    """
    kozmodb_log_level = get_kozmodb_log_level()

    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)

    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    handler = LoggingHandler(level=kozmodb_log_level, logger_provider=logger_provider)

    # Attach OTLP handler to root logger
    logging.getLogger().addHandler(handler)
