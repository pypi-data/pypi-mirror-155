import datetime
import logging
from sca_logger.sca_structured_log import StructuredLog


class SCAFormatter(logging.Formatter):
    def __init__(self, config_params: dict, frmt: str):
        super(SCAFormatter, self).__init__(frmt)
        self.config_params = config_params

    def formatTime(self, record: logging.LogRecord, datefmt=None) -> str:
        timestamp = record.created
        py_datetime = datetime.datetime.fromtimestamp(timestamp)
        return py_datetime.isoformat()

    def format(self, record: logging.LogRecord) -> str or dict:
        """
            Calling super() here will format the record and prepends fields like
            asctime etc. It will also serialize the message field into a string.
            marshal_as_json:
                It will log in splunk as JSON.
                If the message is a json, it will log as a json before invoking super()
                Otherwise, try to convert the message to a json
            string:
                Format to the desired structure passed in __init__ above.
        """
        if self.config_params['marshal_as_json']:
            super(SCAFormatter, self).format(record)
            log = StructuredLog(record)
            if not self.config_params['nest_logs_inside_message']:
                log.promote_message_keys()
            if self.config_params['sanitize_event']:
                log.sanitize_event()
            if self.config_params['clean_up_event']:
                log.clean_up_event()
            return log.get_structured_log()
        else:
            return super(SCAFormatter, self).format(record)
