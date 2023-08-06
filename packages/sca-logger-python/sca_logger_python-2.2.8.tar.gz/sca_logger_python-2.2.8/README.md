

# SCA Logger [![PyPI version](https://badge.fury.io/py/sca_logger_python.svg)](https://badge.fury.io/py/sca_logger_python)

- A library used to collect all the AWS Lambda execution logs to AWS Kinesis
- This is ideal for sending logs to third party applications such as splunk rather than using the native less intuitive cloudwatch

#### Supported Log structures

- String

```txt
[DEBUG] - 2018-12-01 02:27:29,489 - eb4d0cdd-f50f-11e8-8feb-6fda225bd190 - This is end of handle
```

- JSON

```json
{
   "asctime": "2020-04-03T20:53:21.660451",
   "aws_request_id": "b30bbcfa-db6d-4465-8164-c280cc8c6c69",
   "event":{
      "key1":"foo",
      "key2":"bar",
   },
   "filename": "handler.py",
   "funcName": "handle",
   "levelname": "INFO",
   "message": "handled some numbers and logged about it with detailed data",
   "numbers_found": [ 1, 2, 3 ],
   "user_customizable_keys":{
      "anything": "foo",
      "everything": "bar",
   },
}
```


#### Log packaging in kinesis
![picture](image.png)

#### Kinesis Consumer
The consumer to the "sca_logger" kinesis stream is this [Avalon Lambda](https://stash.teslamotors.com/projects/SC/repos/avalon/browse/functions/splunk_log_processor). In case you want to cross-check whether your logs are going to Splunk, you can view your event [here](https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#logEventViewer:group=/aws/lambda/avalon_splunk_log_processor).

This small architecture diagram shows how data (logs) flows through other AWS resources and finally gets POSTed to Splunk endpoint:
https://confluence.teslamotors.com/display/SUC/sca_logger+architecture+diagram

## Usage
- Application trying to log

```python
import logging
from sca_logger import sca_log_decorator

@sca_log_decorator(log_as_json=True, log_event=False, nest_logs_inside_message=False)
def handle(event, context):
   log = logging.getLogger()
   log.info("This is info message")
   log.debug("This is start of handle")
   # application logic
   log.debug("This is end of handle")
   log.info({'message': 'handled some numbers', 'data': (1, 2, 3)})
```

- Application consuming the log from kinesis

```python
import base64
import gzip
import io
import json

def reader(kinesis_event):
    data = kinesis_event['Records'][0]['Data']
    gzipped_bytes = base64.b64decode(data)
    bio = io.BytesIO()
    bio.write(gzipped_bytes)
    bio.seek(0)
    with gzip.GzipFile(mode='rb', fileobj=bio) as gz_reader:
        byte_data = gz_reader.read()
    records = json.loads(byte_data.decode("utf-8"))
    for record in records:
        print(record)
```
- Resulting log structure from the last message

```json
{
  "asctime": "2020-04-03T20:53:21.660451",
  "aws_request_id": "b30bbcfa-db6d-4465-8164-c280cc8c6c69",
  "data": [
    1,
    2,
    3
  ],
  "event": "...",
  "filename": "handler.py",
  "funcName": "handle",
  "levelname": "INFO",
  "message": "handled some numbers"
}
```

## Configuration

  - **MEMORY_HANDLER_LOG_CAPACITY** (defaults to 40)
     Size of the in memory buffer. The library flushes (puts a record in kinesis) if the capacity is hit

  - **KINESIS_SCA_LOG_STREAM***
     Name of the AWS kinesis stream. The application using this library must provide this.

  - **SCA_PRINT_FAILED_LOGS** (defaults to "true")
     Either "true" or "false" - tells us whether to print logs when we fail to post them to Kinesis. 

  - **JSON Logging***
     The ```python @sca_log_decorator``` accepts the following arguments.
     - ```python log_as_json: bool ``` True logs as json. False logs as str. Default is set to True
     - ```python log_event: bool ``` True logs the AWS Lambda event object. False does not log anything in event. Default is set to True
     - ```python nest_logs_inside_message: bool ``` True keeps any json keys logged as sub keys of the "message" key in the final log payload. False makes the json keys that were logged into top level keys in final log payload when possible. Default is set to False
     - ```python sanitize_event: bool ``` True replaces secrets in the `event` with `<SANITIZED>`. Searches any level of the `event` object and overwrites the values of any keys that contain any of these strings (case-insensitive): `authentication, authorization, secret, token, password, cookie`. False leaves the `event` as is. Default is set to True
     - ```python clean_up_event: bool ``` True replaces `stageVariables` and `multiValueHeaders` in the `event` with `<NOT_LOGGED>` to reduce the total number of fields logged. False leaves the `event` as is. Default is set to True



## Tests

```shell
docker-compose build test
docker-compose up test
```

## Package on Pypi
change the version in setup.py
```shell
python setup.py sdist upload -r pypi
```


## Implementation Details
>  Updating shortly!

## Multiprocessing Bug
When using multiprocessing in python, the logs must be manually flushed in two places:
1) On the master process before creating sub-process(es). Failing to do this may result in duplicate logs.
2) At the end of each sub-process. Failing to do this may result in missing logs.

You can manually flush your logs by doing the following:
``` python
LOGGER = logging.getLogger()
# ...
for h in LOGGER.handlers:
   h.flush()
```

## Changelog
* November 15, 2019 (2.1)
   * Added json formatting for string logs, and for raised exceptions that propagate to the decorator
* February 06, 2020 (2.2)
   * Fix an issue causing client handlers importing sca_logger to fail. [7caedb55c01](https://stash.teslamotors.com/projects/SC/repos/sca_logger_python/commits/7caedb55c0121c58c8516b8e9c9157481e2bc36f)
* April 03, 2020 (2.2.2)
   * Change default behavior so that keys in the dict or json string that is logged become top level keys in the log payload.  This prevents `log.info({'message': 'hi', 'info': None})` from resulting in something like `"message": {"message": "hi"}` and instead the log event will have `"message": "hi"` and `"info": null` at the same level as `"asctime"` and and the other top level keys.  Strings that are logged will remain under the top level `"message"` key the same as before.  When logging keys like `"asctime"` that are already in use they will remain nested and the output will have a `"message": {"asctime": ""}` key.
* April 16, 2020 (2.2.3)
  * Fix bug from last release that would cause an exception in sca_structured_log if logging an object that can't be copied
  * Fix bug where % formatting did not work with `log_as_json=True`
  * Add `sanitize_event` feature that is on by default
  * Add `clean_up_event` feature that is on by default
  * Add `lineno` for all logs and a `exc_text` trace back info for exceptions
* April 23, 2020 (2.2.4)
  * Make `sanitize_event` case-insensitive and more strict, e.g. it now sanitizes `userpassword` in addition to `password`
* May 20, 2020 (2.2.5)
  * Updated package metainfo
  * fixed bug where the logger level was always set to DEBUG no matter what
* June 3, 2020 (2.2.6)
  * upgrade the log sanitization function to safely operate when something is unserializable
  * log sanitization will show last few characters when safe
* July 14, 2020 (2.2.7)
  * override the partition key hash to ensure that log events are distributed amongst the Kinesis streams evenly.

### SCA Signature
Project: army_knife

Project Summary: Useful tools for backend

Project Confluence Page: [army_knife](https://confluence.teslamotors.com/display/SCOA/army_knife/)

Repo Summary: Python logger integrate with Splunk.

Repos in the same project:

1. [sca_army_knife.scripts](https://stash.teslamotors.com/projects/SC/repos/sca_army_knife.scripts/browse) Collections of small cli tools and scripts used in CI and local.

2. [sca_army_knife.states](https://stash.teslamotors.com/projects/SC/repos/sca_army_knife.states/browse) Project management states used to organize repos.

3. [lambda-skeleton](https://stash.teslamotors.com/projects/SC/repos/lambda-skeleton/browse) Reference AWS Lambda repo.

4. [sca-sql-queries](https://stash.teslamotors.com/projects/SC/repos/sca-sql-queries/browse) SQL queries from Evan

5. [Iris](https://stash.teslamotors.com/projects/SC/repos/Iris/browse) Buffering for async web requests

6. [avalon](https://stash.teslamotors.com/projects/SC/repos/avalon/browse) Wrapped email notification service.

7. [jammer](https://stash.teslamotors.com/projects/SC/repos/jammer/browse) On-prem proxy to allow access from aws to on-prem resources such as Jira.

PM Owner: @cfreundlich

Code Owner: @vkara