import boto3
import os


def collect_info_for_apps(
    who_am_i: str = None,
    aws_profile=None,
    aws_region=None,
    event_bus_topic: str = None,
    logger=None
):
  if not aws_region:
    if logger:
      logger.debug("Trying to find aws region information from environment AWS_REGION")
    aws_region = os.environ.get('AWS_REGION')
  if not aws_region:
    if logger:
      logger.debug ("Using default aws region: sydney (ap-southeast-2)")
  if not aws_profile:
    if logger:
      logger.debug("Trying to find aws aws profile information from environment AWS_PROFILE")
    aws_profile = os.environ.get('AWS_PROFILE')

  session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
  if not event_bus_topic:
    if logger:
      logger.debug("Trying to find event bus from environment BUSINESS_EVENT_BUS_TOPIC")
    event_bus_topic = os.environ.get('BUSINESS_EVENT_BUS_TOPIC')
  if not event_bus_topic:
    if logger:
      logger.debug("Trying to construct business event bus from account")
    sts_client = session.client('sts')
    client_info = sts_client.get_caller_identity()
    account = client_info.get('Account')
    event_bus_topic = f"arn:aws:sns:{aws_region}:{account}:STPEventBus"
  if not who_am_i:
    if logger:
      logger.debug("Finding whoami from environments WHO_AM_I")
      who_am_i = os.environ.get('WHO_AM_I')
  if not who_am_i:
    if logger:
      logger.debug("Use file name as who_am_i")
    who_am_i = os.path.basename(__file__)
  return dict(
      who_am_i=who_am_i,
      aws_profile=aws_profile,
      aws_region=aws_region,
      event_bus_topic=event_bus_topic,
      session=session
  )
