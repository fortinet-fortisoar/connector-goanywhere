""" Copyright start
  Copyright (C) 2008 - 2023 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

import requests
from connectors.core.connector import ConnectorError, get_logger
from .constant import *

logger = get_logger('goanywhere')


class GoAnywhere(object):
    def __init__(self, config, *args, **kwargs):
        self.username = config.get('username')
        self.password = config.get('password')
        url = config.get('server_url').strip('/')
        if not url.startswith('https://') and not url.startswith('http://'):
            self.url = 'https://{0}/goanywhere/rest/gacmd/v1/'.format(url)
        else:
            self.url = url + '/goanywhere/rest/gacmd/v1/'
        self.verify_ssl = config.get('verify_ssl')

    def make_rest_call(self, url, method, data=None, params=None):
        try:
            url = self.url + url
            headers = {
                'Accept': 'application/json'
            }
            logger.debug("Endpoint {0}".format(url))
            response = requests.request(method, url, data=data, params=params, auth=(self.username, self.password),
                                        headers=headers,
                                        verify=self.verify_ssl)
            logger.debug("response_content {0}:{1}".format(response.status_code, response.content))
            if response.ok or response.status_code == 204:
                logger.info('Successfully got response for url {0}'.format(url))
                if 'json' in str(response.headers):
                    return response.json()
                else:
                    return response
            elif response.status_code == 404:
                return response
            else:
                logger.error("{0}".format(response.status_code, ''))
                raise ConnectorError("{0}".format(response.status_code, response.text))
        except requests.exceptions.SSLError:
            raise ConnectorError('SSL certificate validation failed')
        except requests.exceptions.ConnectTimeout:
            raise ConnectorError('The request timed out while trying to connect to the server')
        except requests.exceptions.ReadTimeout:
            raise ConnectorError(
                'The server did not send any data in the allotted amount of time')
        except requests.exceptions.ConnectionError:
            raise ConnectorError('Invalid Credentials')
        except Exception as err:
            raise ConnectorError(str(err))


def get_groupby(params):
    group_by = params.get('group_by')
    if group_by:
        group_by = GROUP_BY.get(group_by)
    return group_by


def get_date_range(params):
    date_range = params.get('date_range')
    if date_range:
        date_range = DATE_RANGE.get(date_range)
    return date_range


def get_file_transfer_summary(config, params):
    go = GoAnywhere(config)
    endpoint = 'activity/filetransfers/summary'
    group_by = get_groupby(params)
    date_range = get_date_range(params)
    module = params.get('module')
    if module:
        module = FILE_TRANSFER_MODULE.get(module)
    payload = {
        'module': module,
        'date_range': date_range,
        'group_by': group_by
    }
    payload = {k: v for k, v in payload.items() if v is not None and v != ''}
    response = go.make_rest_call(endpoint, 'GET', params=payload)
    return response.get('data')


def get_active_sessions_details(config, params):
    go = GoAnywhere(config)
    endpoint = 'services/sessions'
    services = params.get('services')
    if services:
        services = ACTIVE_SESSIONS_SERVICES.get(services)
    payload = {
        'services': services,
        'max_rows': params.get('max_rows')
    }
    payload = {k: v for k, v in payload.items() if v is not None and v != ''}
    response = go.make_rest_call(endpoint, 'GET', params=payload)
    return response.get('data')


def get_completed_jobs_summary(config, params):
    go = GoAnywhere(config)
    endpoint = 'activity/jobs/completed/summary'
    group_by = get_groupby(params)
    date_range = get_date_range(params)
    status = params.get('status')
    if status:
        status = JOBS_COMPLETED_STATUS.get(status)
    payload = {
        'date_range': date_range,
        'group_by': group_by,
        'status': status
    }
    payload = {k: v for k, v in payload.items() if v is not None and v != ''}
    response = go.make_rest_call(endpoint, 'GET', params=payload)
    return response.get('data')


def _check_health(config):
    try:
        response = get_active_sessions_details(config, params={'max_rows': 1})
        if response:
            return True
    except Exception as err:
        raise ConnectorError("{0}".format(str(err)))


operations = {
    'get_file_transfer_summary': get_file_transfer_summary,
    'get_active_sessions_details': get_active_sessions_details,
    'get_completed_jobs_summary': get_completed_jobs_summary
}
