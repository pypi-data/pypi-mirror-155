import copy
import json
import logging
from sca_logger.sanitize import sanitize


class StructuredLog(object):
    # Used to get a dict with the correct structuring from a LogRecord

    _REQUIRED_JSON_LOG_KEYS = ['event', 'asctime']
    _OPTIONAL_JSON_LOG_KEYS = ['aws_request_id', 'filename', 'funcName', 'levelname',
                               'exc_info', 'exc_text', 'stack_info', 'lineno']
    _SPECIAL_CASE_JSON_LOG_KEYS = ['message']
    _EVENT_CLEAN_UP_KEYS = ['stageVariables', 'multiValueHeaders']

    def __init__(self, record: logging.LogRecord) -> None:
        self._input_record = record
        self._log = {}
        self._generate_log()

    def get_structured_log(self) -> dict:
        return self._log

    def promote_message_keys(self) -> None:
        # Move as many keys as possible from the _log['message'] dict up one level to the _log dict
        # Don't modify the input objects referred to by the LogRecord
        if self.message and type(self.message) is dict:
            non_promoted_keys = self._promote_message_keys_and_return_non_promoted()
            if self._contains_only_message(non_promoted_keys):
                self.message = non_promoted_keys['message']
            elif len(non_promoted_keys) > 0:
                self.message = non_promoted_keys
            else:
                del self.message

    def sanitize_event(self) -> None:
        self._log['event'] = sanitize(self._log['event'])

    def clean_up_event(self) -> None:
        if type(self._log['event']) is dict:
            self._log['event'] = self._make_cleaned_up_copy(self._log['event'])

    def _generate_log(self) -> None:
        self._add_message_key()
        self._add_log_keys()

    def _add_message_key(self) -> None:
        unformatted_message = getattr(self._input_record, 'msg', None)
        if type(unformatted_message) is str:
            formatted_message = self._input_record.getMessage()
            try:
                json_message = json.loads(formatted_message)
                self.message = json_message
            except json.decoder.JSONDecodeError:
                self.message = formatted_message
        else:
            self.message = unformatted_message

    def _add_log_keys(self) -> None:
        for key in self._OPTIONAL_JSON_LOG_KEYS:
            if getattr(self._input_record, key, None):
                self._log[key] = getattr(self._input_record, key)
        for key in self._REQUIRED_JSON_LOG_KEYS:
            self._log[key] = getattr(self._input_record, key, None)

    @classmethod
    def _make_cleaned_up_copy(cls, input: dict) -> dict:
        input_copy = copy.deepcopy(input)
        for key in input:
            if key in cls._EVENT_CLEAN_UP_KEYS:
                input_copy[key] = "<NOT_LOGGED>"
        return input_copy

    def _promote_message_keys_and_return_non_promoted(self) -> dict:
        non_promoted_keys = {}
        for key in list(self.message.keys()):
            if not self._promote_message_key(key):
                non_promoted_keys[key] = self.message[key]
        return non_promoted_keys

    def _promote_message_key(self, key: str) -> bool:
        if not self._is_reserved_key(key):
            self._log[key] = self.message[key]
            return True
        else:
            return False

    @classmethod
    def _contains_only_message(cls, input: dict) -> bool:
        return len(input) == 1 and 'message' in input

    @classmethod
    def _is_reserved_key(cls, key: str) -> bool:
        return key in cls._REQUIRED_JSON_LOG_KEYS + cls._OPTIONAL_JSON_LOG_KEYS + cls._SPECIAL_CASE_JSON_LOG_KEYS

    @property
    def message(self):
        return self._log['message']

    @message.setter
    def message(self, message):
        self._log['message'] = message

    @message.deleter
    def message(self):
        del self._log['message']
