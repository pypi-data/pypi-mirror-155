import logging
import copy
import json

LOGGER = logging.getLogger()
DANGEROUS = {'password', 'secret', 'auth', 'token', 'cookie', 'key'}
AUTH_PREFIX = 'Bearer'


def sanitize(blob, key=''):
    copy_blob = _safe_copy(blob)
    return _recursive_sanitize(copy_blob)


def _safe_dict_copy(blob) -> dict:
    return {k: _safe_copy(v) for k, v in blob.items()}


def _safe_list_tuple_copy(blob) -> list:
    return [_safe_copy(v) for v in blob]


def _safe_blind_copy(blob):
    try:
        return copy.deepcopy(blob)
    except Exception as the_error:
        # print(f'Encountered {the_error} serializing {blob}.' +
        #       ' Converting to string.')
        return str(blob)


def _safe_copy(blob):
    if isinstance(blob, dict):
        return _safe_dict_copy(blob)
    if isinstance(blob, (list, tuple)):
        return _safe_list_tuple_copy(blob)
    return _safe_blind_copy(blob)


def _recursive_sanitize(blob, key=''):
    if isinstance(blob, dict):
        return _dict_sanitize(blob)
    if isinstance(blob, list):
        return _list_sanitize(blob)
    if isinstance(blob, (str, int)):
        if _safe_to_log(key=key, value=blob):
            return blob
        return _value_sanitize(str(blob))
    # print(f'Cannot sanitize objects of type: {type(blob)}')
    return blob


def _value_sanitize(a_string: str):
    a_string = str(a_string)
    if _is_auth_token(a_string):
        return f'{AUTH_PREFIX} {_redact(_extract_token(a_string))}'
    return _redact(a_string)


def _list_sanitize(the_list: list):
    for this_index, item in enumerate(the_list):
        the_list[this_index] = _recursive_sanitize(blob=item)
    return the_list


def _dict_sanitize(blob: dict):
    for k, v in blob.items():
        blob[k] = _recursive_sanitize(blob=v, key=k)
    return blob


def _is_auth_token(a_string: str):
    contains_prefix = a_string.lower().startswith(AUTH_PREFIX.lower())
    has_something_else = len(a_string) > len(AUTH_PREFIX)
    return contains_prefix and has_something_else


def _extract_token(a_string: str):
    if not _is_auth_token(a_string):
        raise ValueError('Auth prefix not found in token.')
    prefix_length = len(AUTH_PREFIX)
    if a_string[prefix_length] == ' ':
        prefix_length += 1
    return a_string[prefix_length:]


def _safe_to_log(key, value):
    if any(d in key.lower() for d in DANGEROUS):
        return False
    if not isinstance(value, str):
        return True
    if _is_auth_token(value):
        return False
    return True


def _redact(pw: str):
    if len(pw) > 8:
        return f'----{pw[-4:]}'
    if len(pw) > 5:
        return f'----{pw[-2:]}'
    return '----'
