#!/usr/bin/env python3
import click
import click_log
import logging
import boto3
import datetime
import os
import time
import json
from sonder_common import collect_default
from sonder_common import multi_threading
import threading
log = logging.getLogger(__name__)
click_log.basic_config(log)


# This global info might be used with multiple threading enviroment.
# Think careful of concurrency.
global_info = {
  'session_info':None
} 

# @multi_threading.threaded
def report_event(
    _type: str,
    action: str,
    success: bool = True,
    version: str = '1.0',
    sonder_meta_info: dict = dict(),
    body: dict = dict(),
    who_am_i: str = None,
    logger=None,
    aws_profile=None,
    aws_region=None,
    event_bus_topic: str = None,
):
  """Report STP formatted events

  Event format can be found
  https://sonderaustralia.atlassian.net/wiki/spaces/DEV/pages/1387267127/STP+BusinessEventBus
  """
  global global_info
  if not global_info['session_info']:
    global_info['session_info'] = collect_default.collect_info_for_apps(
        aws_profile=aws_profile,
        aws_region=aws_region,
        who_am_i=who_am_i,
        event_bus_topic=event_bus_topic,
        logger=logger,
    )
  sys_info=global_info['session_info']
  sns_client = sys_info['session'].client('sns', region_name=sys_info.get('aws_region'))
  if logger:
    logger.debug(f"Event ({_type}, {action}) to be reported to {sys_info.get('event_bus_topic')} with body {body} ")
  sns_result = sns_client.publish(
      TopicArn=sys_info.get('event_bus_topic'),
      Message=json.dumps({
          "time": int(time.time()) * 1000,
          "type": _type,
          "source_id": sys_info.get('who_am_i'),
          "action": action,
          "body" : body,
          'result': {
              "success": success,
          },
          'version': version,
          'sonder_meta_info': sonder_meta_info
      }),
      MessageAttributes={
          'type': {
              'DataType': 'String',
              'StringValue': _type,
          },
          'action': {
              'DataType': 'String',
              'StringValue': action,
          },

      },
  )

  if logger:
    logger.info(f"Event ({_type}, {action}) reported to {sys_info.get('event_bus_topic')} ")


@click.command()
@click.option('--profile', '-p', help='The profile', default=None)
@click.option('--region', '-r', help='The AWS region', default='ap-southeast-2')
@click.option('--source_id', '-s', help='The source_Id', default=None)
@click.option('--event-type', '-t', help='Them event type', required=True)
@click.option('--event-action', '-a', help='The event action', required=True)
@click.option('--success/--no-success', '-S', help='Is the event succeded.', default=True)
@click.option('--event-body', '-b', help='The event body. Must be a string of dictionary.', default='{}')
@click.option('--event-version', '-ev', help='The event version.', default='1.0')
@click.option('--sonder-meta-info', '-m', help='The event meta info, including x-sonder-trace-id, aws-xray-id, etc.. Must be a string of dictionary.', default='{"x-sonder-trace-id":""}')
@click_log.simple_verbosity_option(log)
def report(profile, region, source_id, event_type, event_action, success,
           event_version, event_body, sonder_meta_info):
  """Report an event
  The event format can be found at 
    https://sonderaustralia.atlassian.net/wiki/spaces/DEV/pages/1387267127/STP+BusinessEventBus

  """

  report_event(
      event_type, event_action,
      success=success,
      version=event_version,
      sonder_meta_info=json.loads(sonder_meta_info),
      body=json.loads(event_body),
      who_am_i=source_id,
      logger=log,
      aws_profile=profile,
      aws_region=region,
  )

if __name__ == '__main__':
  report()
