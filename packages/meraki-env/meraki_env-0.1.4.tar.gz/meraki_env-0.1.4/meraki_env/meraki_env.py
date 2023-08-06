# from dotenv import load_dotenv
#
# load_dotenv()
import os


def meraki_api_key():
    key = os.getenv('meraki_api_key', None)
    if key is None:
        raise SystemExit('Please set environment variable meraki_api_key')
    else:
        key = os.environ['meraki_api_key']
    return key


def meraki_organization_id():
    organization_id = os.getenv('meraki_organization_id', None)
    if organization_id is None:
        raise SystemExit('Please set environment variable meraki_organization_id')
    else:
        organization_id = os.environ['meraki_organization_id']
    return organization_id


def meraki_base_url():
    base_url = os.getenv('meraki_base_url', None)
    if base_url is None:
        raise SystemExit('Please set environment variable meraki_base_url')
    else:
        base_url = os.environ['meraki_base_url']
    return base_url
