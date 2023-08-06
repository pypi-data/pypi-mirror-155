from __future__ import absolute_import, division, print_function, unicode_literals

import os
import tempfile
from collections import defaultdict, OrderedDict
import datetime
import functools
import time
import sys
from logging import getLogger
import re
from requests.compat import urlencode

from .hooks.base import Request, Response, BaseHook
from .points_serializers import shooju_point, NANOSECONDS, Point, milli_tuple
from .common import *
import requests
from itertools import cycle

__version__ = '3.8.0'

if NUMPY_INSTALLED:
    from .points_serializers import np_array

if PANDAS_INSTALLED:
    from .points_serializers import pd_series, pd_series_localized


KEY_RE = re.compile(r'\{([\w\d\.]+)}')

LOCATION_TYPE = 'python'

if sys.version_info[0] >= 3:
    basestring = str

DEFAULT_REQUEST_TIMEOUT = 600.


# global lib options
class Options(object):

    def __init__(self, disable_sjts=False, disable_msgpack=False,
                 points_serializer=shooju_point, return_series_errors=False):
        self._disable_sjts = self._disable_msgpack = None
        self.series_serializer = self.default_serializer = None
        self.point_serializer = points_serializer
        self.return_series_errors = return_series_errors

        self._set_serializers(disable_sjts=disable_sjts, disable_msgpack=disable_msgpack)

    @staticmethod
    def _get_serializer(disable_sjts=True, disable_msgpack=True):
        if not disable_sjts and sjts is None:
            raise Exception('sjts module is not installed')
        elif not disable_msgpack and msgpack is None:
            raise Exception('msgpack module is not installed')

        if not disable_sjts:
            return sjts
        elif not disable_msgpack:
            return msgpack
        return json_serializer

    def _set_serializers(self, disable_sjts=None, disable_msgpack=None):
        disable_sjts = self._disable_sjts if disable_sjts is None else disable_sjts
        disable_msgpack = self._disable_msgpack if disable_msgpack is None else disable_msgpack

        self.default_serializer = self._get_serializer(disable_msgpack=disable_msgpack)
        self.series_serializer = self._get_serializer(disable_sjts=disable_sjts, disable_msgpack=disable_msgpack)

        self._disable_sjts = disable_sjts
        self._disable_msgpack = disable_msgpack

    @property
    def disable_sjts(self):
        return self._disable_sjts

    @disable_sjts.setter
    def disable_sjts(self, value):
        self._set_serializers(disable_sjts=value)

    @property
    def disable_msgpack(self):
        return self._disable_msgpack

    @disable_msgpack.setter
    def disable_msgpack(self, value):
        self._set_serializers(disable_msgpack=value)

    @property
    def point_serializer(self):
        return self._point_serializer

    @point_serializer.setter
    def point_serializer(self, val):
        assert callable(val), 'point_serializer must be callable'
        self._point_serializer = val


options = Options(disable_sjts=sjts is None, disable_msgpack=msgpack is None, return_series_errors=False)

logger = getLogger('shooju_client')


class ConnectionError(Exception):
    """
    Connection Errors
    """
    pass


class ShoojuApiError(Exception):
    """
    Shooju API errors
    """

    def __init__(self, message=''):
        super(ShoojuApiError, self).__init__(message)
        self.message = message


def sid(*args):
    """
    Constructs a series id using the list of arguments

    :param args: parts of the series id
    :return: formatted series id
    :rtype: str
    """
    return "\\".join(args)


class SeriesRespone(object):
    """
    Represents an API response to series request
    """
    def __init__(self, response):
        self.success = None
        self.total = None
        self.series = list()
        self.included_job = None
        self.included_timestamp = None
        self.request_id = None
        if 'success' in response:
            self.success = response['success']
        if 'total' in response:
            self.total = response['total']
        if 'series' in response:
            self.series = response['series']
        if 'included_job' in response:
            self.included_job = response['included_job']
        if 'included_timestamp' in response:
            self.included_timestamp = response['included_timestamp']
        if 'request_id' in response:
            self.request_id = response['request_id']

    @property
    def first_series(self):
        """
        :return: dict with series and meta attributes such as included_job and included_timestamp
        """
        return {'series': self.series[0], 'included_job': self.included_job,
                'included_timestamp': self.included_timestamp}

class Connection(object):
    """
    Represents a Connection to the Shooju api
    """

    def __init__(self, server, *args, **kwargs):
        """
        Initializes connection to the Shooju API.
        Must use either user+api_key or email+google_oauth_token to authenticate.

        :param str user: Shooju username
        :param api_key: Shooju API key
        :param google_oauth_token: Google API refresh token
        :param email: Google account email
        :param server: Shooju server with protocol (https://alpha2.shooju.com) or just account name (alpha2).
        :param retries: Number of attempts to execute api call
        :param retry_delay: Time between api call attempts (seconds)
        :param location: Connection location name
        :param hosts: Array of Shooju API endpoints. Used when access by ip, or different host name.
        :param requests_session: session object of requests.Session type to use as transport
        :param extra_params: default query parameters added to all client requests to the server
        :param timeout: request timeout
        :params hooks: A list of API hooks
        """
        self.shooju_api = ShoojuApi(server, *args, **kwargs)

    @property
    def user(self):
        """
        Returns current user.
        """
        return self.shooju_api.client._user

    @property
    def raw(self):
        """
        Retrieves a REST client to perform arbitrary requests to the Shooju API.

        Usage:
            conn.raw.get('/teams/', params={'q': 'test'})
            conn.raw.post('/teams/myteam/', data_json={'description': 'description'})
            conn.raw.delete('/alerts/topics/series/types/alert')

        :return: shooju.Client instance
        """
        return self.shooju_api.client

    def get_series(self, series_query, fields=None, df=None, dt=None, max_points=0,
                   extra_params=None, serializer=None, ):
        """
        Retrieves fields and points for a series query. Can select time range. If series does not exist returns
        None

        :param str series_query: query that returns 1 series
        :param fields: list of fields to retrieve; use ['*'] for all non-meta
        :param df: date FROM for points; can be datetime(), date(), 'MAX', 'MIN', or relative date format
        :param dt: date TO for points; can be datetime(), date(), 'MAX', 'MIN', or relative date format
        :param max_points: number of points to retrieve per series; use -1 for all
        :param dict extra_params: extra parameters; refer to API Documentation
        :param serializer: points serializer function; use one of shooju.points_serializers.*
        :return: series dict with series_id and optional points and fields keys
        """
        serializer = options.point_serializer if serializer is None else serializer
        deserialize_response_to_numpy = _deseralize_points_response_directly_to_numpy(serializer)

        data = self.shooju_api.get_single_series(series_query=series_query, df=df, dt=dt,
                                                 max_points=max_points,
                                                 fields=fields,
                                                 extra_params=extra_params,
                                                 deserialize_response_to_numpy=deserialize_response_to_numpy)
        series = data.get('series')
        # Adding extra parameters to series request
        meta_attributes = {k: data[k] for k in ('included_job', 'included_timestamp')}
        if series and 'points' in series:
            series['points'] = serializer(series['points'],
                                                  tz=self._extract_series_tz(series), **meta_attributes)
        return series

    def scroll(self, query='', fields=None, df=None, dt=None, max_points=0,
                sort=None, serializer=None, max_series=None, extra_params=None,
                scroll_batch_size=2500):
        """
        Performs a scroll search. Function is a generator, yields series

        Usage::

            for series in conn.scroll_series():
                # do something with the dict

        :param str query: query that returns 0+ series
        :param list fields: list of fields to retrieve; use ['*'] for all non-meta
        :param df: date FROM for points; can be datetime(), date(), 'MAX', 'MIN', or relative date format
        :param dt: date TO for points; can be datetime(), date(), 'MAX', 'MIN', or relative date format
        :param int max_points: number of points to retrieve per series; use -1 for all
        :param str sort: field(s) to sort on, formatted as a string with <FIELD> and <DIRECTION> pairs separated by commas, where <DIRECTION> is one of "asc" or "desc". For example, sorting in descending order on amount: "amount desc" or sorting in descending order on state and ascending order on city: "state desc, city asc".
        :param function serializer: points serializer function; use one of shooju.points_serializers.*
        :param int max_series: maximum number of series to return
        :param dict extra_params: extra parameters; refer to API Documentation
        :param int scroll_batch_size: number of series to retrieve per single API request

        """

        scroll = max_series is None or max_series > scroll_batch_size

        serializer = options.point_serializer if serializer is None else serializer
        deserialize_response_to_numpy = _deseralize_points_response_directly_to_numpy(serializer)

        r = self.shooju_api.search_series(query, df, dt, max_points=max_points,
                                          fields=fields, scroll=scroll,
                                          scroll_batch_size=scroll_batch_size if scroll else None, sort=sort,
                                          deserialize_response_to_numpy=deserialize_response_to_numpy,
                                          url_params=extra_params, per_page=max_series if not scroll else None)
        scroll_id = r.get('scroll_id') if scroll else None
        series_left = r['total'] if scroll else min(max_series, r['total'])

        while series_left > 0:
            if not r['series']:
                break
            if not options.return_series_errors:
                _check_bulk_api_errors(r['series'])
            for s in self._process_search_response(r, serializer):
                yield s
            series_left -= len(r['series'])
            if series_left:
                r = self.shooju_api.scroll_series(scroll_id)

    def get_points(self, series_id, date_start=None, date_finish=None, max_points=10,
                   size=None, serializer=None):
        """
        Long-term deprecated; get_series() using query sid="{series_id}" instead.

        Retrieves points for a series id. Can select time range. If series does not exist returns
        None

        :param str series_id: series id
        :param datetime.datetime date_start: get points < date
        :param datetime.datetime date_finish: get points > date
        :param int size: number of points to get
        :param int max_points: number of points to get
        :param int size: number of points to get (this parameter is deprecated, use max_points)
        :param serializer: points serializer function; use one of shooju.points_serializers.*
        :return: points represented by `serializer` type
        :rtype: list, numpy.array, pandas.Series
        """
        if size is not None:
            max_points = size
        serializer = options.point_serializer if serializer is None else serializer
        deserialize_response_to_numpy = _deseralize_points_response_directly_to_numpy(serializer)

        data = self.shooju_api.get_single_series(series_id=series_id, df=date_start, dt=date_finish,
                                                 max_points=max_points,
                                                 deserialize_response_to_numpy=deserialize_response_to_numpy)['series']

        return serializer(data.get('points', []), tz=self._extract_series_tz(data)) if data is not None else None

    def get_fields(self, series_id, fields='*'):
        """
        Long-term deprecated; get_series() using query sid="{series_id}" instead.

        Retrieves fields from series. Parameter `fields` is a list of field names. If `fields` is not
        present, all of the fields are returned

        :param str series_id: series id
        :param list fields: list of fields to retrieve
        :return: fields of the series
        :rtype: dict
        """
        data = self.shooju_api.get_single_series(series_id=series_id, size=0, fields=fields,)['series']
        if data is None:
            return None
        return data.get('fields', {})

    def get_reported_dates(self, series_query=None, job_id=None, processor=None, df=None, dt=None, mode='points'):
        """
        Retrieves reported dates for one of the following (use only one): series_query, job_id, processor.  Dates returned can be limited via df/dt.

        :param series_query: returns reported dates written for that series
        :param job_id: return reported dates written by that job
        :param processor:  return reported dates for series written by that processor
        :param df: datetime to start the dates array
        :param dt: datetime to finish the dates array
        :param mode: return either `points` or `fields` reported dates
        :return: list of reported dates
        """
        reported_dates = self.shooju_api.get_reported_dates(series_query=series_query, job_id=job_id,
                                                            processor=processor, df=df, dt=dt,
                                                            mode=mode).get('reported_dates') or []
        return list(map(milli_to_datetime, reported_dates))

    def register_job(self, description, notes="", batch_size=1,
                     dry_run=False):
        """
        Registers a job in Shooju. A job is used to write series.

        :param str description: brief description
        :param str notes: notes about the job
        :param int batch_size: indicates the size of the buffer before creating new series in the server
        :param bool dry_run: if True data will no be send to Shooju. it just will be printed.
        :return: a RemoteJob instance
        :rtype: shooju.RemoteJob
        """
        if len(description) < 3:
            raise ValueError('description should be longer than 3 characters')

        if not dry_run:
            data = self.shooju_api.register_job(description, notes)
            return RemoteJob(
                self, data['job_id'], batch_size=batch_size, collision_retry_timeout=10.0)
        else:
            return DryRunJob(self, None, batch_size=batch_size, collision_retry_timeout=10.0)

    def create_uploader_session(self):
        """
        DEPRECATED: use Connection.upload_file() instead.

        Registers an uploader session.

        Used for uploading files to Shooju.

        :return: a UploaderSession instance
        :rtype: shooju.UploaderSession
        """
        return UploaderSession(self)

    def mget(self):
        """
        Creates a multiget object to perform requests in batch
        """
        return GetBulk(self)

    def download_file(self, file_id, filename=None):
        """
        Downloads a file. If no `filename` is provided, a temporary file is created

        :param file_id: file id
        :param filename: file name for downloaded file
        :return: File instance
        """
        return self.shooju_api.download_file(file_id, filename)

    def _process_search_response(self, data, serializer):
        """
        Helper method to convert a api series search response to the module data structures
        :param data: api series response
        :param serializer: points serializer function; use one of shooju.points_serializers.*
        :return: array of series objects
        :rtype: list
        """
        results = list()
        for s in data['series']:
            s.setdefault('fields', {})
            if 'points' in s:
                s['points'] = serializer(s['points'], tz=self._extract_series_tz(s))
            results.append(s)
        return results

    def _extract_series_tz(self, ser):
        return ser.get('tz', {}).get('timezone')

    def get_df(self, query, fields, series_axis='rows', df=None, dt=None, max_points=0, sort=None, max_series=None,
               extra_params=None, scroll_batch_size=2500):
        """
        Returns Pandas DataFrame; uses scroll() under the hood. All date indexes returned are tz-aware, to strip use Connection.get_df(.....).tz_localize(None)
        :param query: query that returns 1+ series; required non-empty
        :param fields: list of fields to retrieve; 1+ fields required; if series_axis is 'columns' and multiple fields are requested, values will be joined by /
        :param series_axis: 'rows' returns series in the rows and fields in the columns; 'columns' returns each series as a column identified by fields param and dates in the rows
        :param df: date FROM for points; can be datetime(), date(), 'MAX', 'MIN', or relative date format
        :param dt: date TO for points; can be datetime(), date(), 'MAX', 'MIN', or relative date format
        :param max_points: number of points to retrieve per series; use -1 for all
        :param sort: field(s) to sort on; formatted as comma-delimited list of <FIELD> <DIRECTION> where <DIRECTION> is one of "asc" and "desc".
        :param max_series: maximum number of series to return
        :param extra_params: extra parameters; refer to API Documentation
        :param scroll_batch_size: number of series to retrieve per single API request
        """

        if not pandas:
            raise ShoojuApiError('Pandas has to be installed in order to generate dataframe.')

        # deep copy of function args
        scroll_args = { k: v for k, v in locals().items() if k != 'self'}
        series_axis = scroll_args.pop('series_axis')

        response = self.scroll(serializer=pd_series_localized, **scroll_args)
        if series_axis == 'columns':
            base_data = defaultdict(lambda: pandas.Series([], index=pandas.DatetimeIndex([], tz='UTC'), dtype='float64'))
            for series in response:
                column_header = series['series_id']
                if series.get('fields'):
                    # if '*' is entered to get all fields, use description as default
                    # else if multiple fields are requested, values will be joined by /
                    all_fields = True if '*' in fields else False
                    if all_fields and series['fields'].get('description'):
                        column_header = series['fields'].get('description')
                    else:
                        column_header = '/'.join([str(series['fields'].get(_field, 'None')) for _field in fields])
                base_data[column_header] = base_data[column_header].append(to_append=series.get('points', list()))
        else:
            base_data = list()
            if max_points != 0:
                def _iter_rows():
                    for series in response:
                        flds = series.get('fields', dict())
                        if 'points' not in series or series['points'].empty:
                            continue
                        for _date, _point in series['points'].items():
                            row = dict(flds)
                            row.update({'dt': _date, 'val': _point, 'series_id': series['series_id']})
                            yield row
                base_data = sorted(_iter_rows(), key=lambda x: x['dt'])
            else:
                # Prepare data for dataframe with only fields
                for series in response:
                    base_data.append(dict(series_id=series['series_id'], **series.get('fields', dict())))

        return pandas.DataFrame(data=base_data)

    def upload_file(self, fp, filename, custom_fields=None):
        """
        Uploads a file object to Shooju. Returns the Shooju file id.

        :param fp: File Object to upload
        :param filename: Name of the file.  For cosmetic/retrieval purposes only.
        :param custom_fields: A dict with file's custom fields
        """
        data = self.raw.post(
            '/files',
            files={'file': (filename, fp)},
            data={'meta': json.dumps({'custom': custom_fields})} if custom_fields else None
        )
        return data['file_id'][0]

    def init_multipart_upload(self, filename, custom_fields=None):
        """
        Initiates multipart upload to upload big files by its parts.

        :param filename: Name of the file.
        :param custom_fields: A dict with file's custom fields
        :return: MultiPartUploader
        """
        payload = {'filename': filename}

        if custom_fields:
            payload['custom'] = custom_fields

        data = self.raw.post(
            '/files/multipart/init',
            data_json=payload
        )

        return MultiPartUploader(self, data['file_id'])


def _parse_dt(d, param_name, default):
    if d is not None and not isinstance(d, six.string_types):
        try:
            d = to_milli(d)
        except ValueError:
            raise ValueError("{} accepts only string, milliseconds since epoch, datetime.date,"
                             " or datetime.datetime objects".format(param_name))
    elif d is None:
        d = default
    return d


class ShoojuApi(object):
    """
    Class used to encapsulate Shooju API methods. Methods return the json decoded response from the server and raise
    an error if the response had errors.
    """

    API_SERIES = '/series'
    API_SERIES_WRITE = '/series/write'
    API_SERIES_DELETE = '/series/delete'
    API_REPORTED_DATES = '/series/reported_dates'
    API_REPORTED_DATES_DELETE = '/series/reported_dates/delete'
    API_JOBS = '/jobs/'
    API_FILES = '/files/{id}/download'
    API_STATUS = '/status/green'
    API_PING = '/status/ping'
    API_GOOGLE_OAUTH = '/auth/googleoauth'

    def __init__(self, server, *args, **kwargs):
        server = server if server.startswith('http') else 'https://{}.shooju.com'.format(server)
        if len(args) >= 2:
            user, api_key = args[:2]
        else:
            user, api_key = kwargs.get('user'), kwargs.get('api_key')
        requests_session = kwargs.get('requests_session')
        if not all((user, api_key)):
            email = kwargs.get('email', os.environ.get('SHOOJU_EMAIL'))
            google_auth_token = kwargs.get('google_oauth_token', os.environ.get('SHOOJU_GOOGLE_OAUTH_TOKEN'))

            if email and google_auth_token:
                anonymous_client = Client(server, location=kwargs.get('location'),
                                          requests_session=requests_session)
                credentials = anonymous_client.post(self.API_GOOGLE_OAUTH,
                                                    data_json={'token': google_auth_token,
                                                               'email': email})
                user, api_key = credentials['user'], credentials['api_secret']

        if not all((user, api_key)):
            raise ShoojuApiError('Must use either user+api_key or email+google_oauth_token to authenticate.')

        self.client = Client(server, user, api_key,
                             retries=kwargs.get('retries'),
                             retry_delay=kwargs.get('retry_delay'),
                             location=kwargs.get('location'),
                             hosts=kwargs.get('hosts'),
                             requests_session=requests_session,
                             timeout=kwargs.get('timeout'),
                             extra_params=kwargs.get('extra_params', {}),
                             hooks=kwargs.get('hooks'))

    def get_single_series(self, series_id=None, series_query=None, df=None, dt=None,
                          max_points=None, fields=None, deserialize_response_to_numpy=None,
                          extra_params=None, **kwargs):
        """
        Retrieves series

        :param str series_id: series id
        :param str series_query: series query
        :param datetime.datetime df: start date for points
        :param datetime.datetime dt:  end date for points
        :param int max_points: number of points to retrieve
        :param list fields: list of fields to retrieve
        :param deserialize_response_to_numpy: if True will deserialize sjts body into numpy points array
        :param dict extra_params: extra url parameters to pass to api call
        :return: api response
        :rtype: dict
        """
        assert series_id or series_query, 'either one of series_id, series_query must be passed'
        max_points = max_points or kwargs.get('size')
        return self.series_read(series_ids=[series_id] if series_id is not None else None,
                                series_queries=[series_query] if series_query is not None else None,
                                df=df, dt=dt, max_points=max_points,
                                fields=fields, deserialize_response_to_numpy=deserialize_response_to_numpy,
                                extra_params=extra_params).first_series

    def series_read(self, series_ids=None, series_queries=None, series_requests=None,
                    df=None, dt=None, max_points=None, fields=None, deserialize_response_to_numpy=None,
                    extra_params=None):
        """
        Executes series read request

        :param list series_ids: array of series ids to fetch
        :param list series_queries: array of series queries ids to fetch
        :param list series_requests: array of series ids and its parameters
        :param datetime.datetime df: start date for points
        :param datetime.datetime dt:  end date for points
        :param int max_points: number of points to retrieve
        :param list fields: list of fields to retrieve
        :param deserialize_response_to_numpy: if True will deserialize sjts body into numpy points array
        :param dict extra_params: extra url parameters to pass to api call
        :return: api response
        :rtype: SeriesRespone
        """
        deserializer_params = dict()
        if deserialize_response_to_numpy:
            deserializer_params['use_numpy'] = True
        url_params = {
            'date_format': 'milli',
            'df': _parse_dt(df, 'df', 'MIN') if df is not None else None,
            'dt': _parse_dt(dt, 'dt', 'MAX') if dt is not None else None,
        }

        if fields is not None:
            url_params['fields'] = ','.join(fields)

        if max_points is not None:
            url_params['max_points'] = max_points

        if extra_params:
            url_params.update(extra_params)
        client_kwargs = {
            'deserializer': options.series_serializer,
            'deserializer_params': deserializer_params,
            'params': url_params
        }

        if series_ids is not None:
            data_json = {'series_ids': series_ids}
        elif series_requests is not None:
            data_json = {'series': series_requests}
        elif series_queries is not None:
            data_json = {'series_queries': series_queries}
        else:
            raise AssertionError('either one of the following parameters must be passed: '
                                 'series_ids, series_ids_requests, series_queries')
        client_kwargs['data_json'] = data_json

        response = self.client.post('/series', **client_kwargs)
        if not options.return_series_errors:
            _check_bulk_api_errors(response['series'])
        return SeriesRespone(response)

    def series_write(self, data, job_id=None, collision_retry_timeout=60,
                     async_mode=False, skip_meta_if_no_fields=False):
        """
        Writes series data

        :param list data: array of series objects to write
        :param int job_id: job id
        :param float collision_retry_timeout: lock write timeout
        :param bool async_mode: indicates that fields should be written asynchronously
        :param bool skip_meta_if_no_fields: indicates that write api will not write points meta if no field written
        """
        deserializer = options.default_serializer
        serializer = options.series_serializer

        # by this logic we trying to retry failed sub-requests and bring all responses together in to same order
        req_by_index = {i: r for i, r in enumerate(data)}
        resp_by_index = {}
        params = {k: v for k, v in {'job_id': job_id,
                                    'async_mode': async_mode,
                                    'date_format': 'milli',
                                    'skip_meta_if_no_fields': skip_meta_if_no_fields}.items() if k}

        req_index_to_send = req_by_index.keys()
        attempts_left = 3

        while req_index_to_send and attempts_left:
            req_index_to_send = sorted(req_index_to_send)
            req_index_to_send_again = list()
            attempts_left -= 1

            requests_to_send = [req_by_index[r] for r in req_index_to_send]
            payload = {'series': requests_to_send}
            response = self.client.post('/series/write', data_json=payload,
                                        params=params, deserializer=deserializer, serializer=serializer)
            for i, resp in enumerate(response['responses']):
                if not self._can_retry(resp) or not attempts_left:  # this is either success or final attempt
                    resp_by_index[req_index_to_send[i]] = resp
                else:
                    logger.debug(u'retrying bulk request because of: {error} {description}'.format(**resp))
                    req_index_to_send_again.append(req_index_to_send[i])  # we will try this again
            req_index_to_send = req_index_to_send_again
            if attempts_left and req_index_to_send:
                time.sleep(collision_retry_timeout)
        responses = [r[1] for r in sorted(resp_by_index.items(), key=lambda x: x[0])]
        _check_bulk_api_errors(responses)
        return responses

    @staticmethod
    def _can_retry(resp):
        """
        Returns True if error in response can be retried.
        """
        if resp.get('error') and 'series is locked for change' in resp.get('description', ''):
            return True
        else:
            return False

    def delete_series_by_query(self, query, force=False, job_id=None):
        """
        Permanently deletes all series that match the query - be careful

        :param query: query to base the deletion on
        :param force: if True permanently deletes without moving to trash
        :param job_id: job id to associate with deleted series
        :return: number of series deleted
        """
        return self.client.delete(self.API_SERIES_DELETE,
                                  data_json={'query': query, 'force': force, 'job_id': job_id})['deleted']

    def register_job(self, description, notes='', source='python'):
        """
        Registers a job in Shooju.

        :param str description: brief description
        :param str notes: notes about the job
        :param str source: source of the job
        :return: api response
        :rtype: dict
        """
        payload = {
            "source": source,
            "description": description,
            "notes": notes
        }
        data = self.client.post(self.API_JOBS, data_json=payload)
        return data

    def download_file(self, file_id, filename=None):
        """
        Downloads a file. If no `filename` is provided, a temporary file is created

        :param file_id: file id
        :param filename: file name for downloaded file
        :return: File instance
        """
        path = self.API_FILES.format(id=file_id)
        if filename:
            f = open(filename, 'w+b')
        else:
            f = tempfile.NamedTemporaryFile(prefix='download')

        r = self.client.get(path, binary_response=True)

        for chunk in r.iter_content(chunk_size=16 * 1024):
            if chunk:
                f.write(chunk)
                f.flush()
        f.seek(0, 0)
        return f

    def search_series(self, query='', date_start=None, date_finish=None, max_points=0,
                      scroll_batch_size=None, per_page=None, fields=None, scroll=False, sort_on=None,
                      sort_order='asc', operators=None, size=None, query_size=None, sort=None,
                      deserialize_response_to_numpy=None, url_params=None):
        """
        Performs a search request to the shooju api

        :param query: query string
        :param date_start: points start date
        :param date_finish: points end date
        :param max_points: number of points
        :param size: number of  (deprecated parameter)
        :param scroll_batch_size: number of series to retrieve per scroll request
        :param per_page: number of series to retrieve per page
        :param query_size: number of series to retrieve (deprecated)
        :param fields: list of fields to retrieve
        :param scroll: flag indicating if it's a scroll search
        :param sort_on: field name to sort series on
        :param sort_order: sort direction
        :param scroll: flag indicating if it's a scroll search
        :param operators: array of series operators
        :param deserialize_response_to_numpy: if True will deserialize sjts body into numpy points array
        :param url_params: additional url_params
        :return: dict with the api response
        """
        if size is not None:
            max_points = size

        deserializer_params = dict()
        if deserialize_response_to_numpy:
            deserializer_params['use_numpy'] = True

        params = {
            'query': query,
            'date_format': 'milli',
            'df': _parse_dt(date_start, 'date_start', 'MIN'),
            'dt': _parse_dt(date_finish, 'date_finish', 'MAX'),
            'max_points': max_points,
        }

        if fields:
            params['fields'] = ','.join(fields)

        if scroll_batch_size is not None:
            params['scroll_batch_size'] = scroll_batch_size

        if per_page:
            params['per_page'] = per_page

        if query_size:
            params.update({
                'scroll_batch_size': query_size,
                'per_page': query_size
            })

        if scroll:
            params['scroll'] = 'y'

        if sort:
            params['sort'] = sort
        elif sort_on:
            params['sort'] = '{} {}'.format(sort_on, sort_order)

        if operators:
            params['operators'] = '@{}'.format('@'.join(operators))

        if url_params:
            params.update(url_params)

        return self.client.get(self.API_SERIES, deserializer=options.series_serializer, params=params,
                               deserializer_params=deserializer_params)

    def get_reported_dates(self, series_query=None, job_id=None, processor=None,
                           df=None, dt=None, mode='points'):
        """
        Retrieves reported dates.

        :param series_query: returns reported dates written for that series
        :param job_id: return reported dates written by that job
        :param processor:  return reported dates for series written by that processor
        :param df: datetime to start the dates array
        :param dt: datetime to finish the dates array
        :param mode: return either `points` or `fields` reported dates
        :return: list of reported dates
        """
        assert series_query or job_id or processor, \
            'At least one of series_query, job_id or processor parameters required'
        params = {
            'series_query': series_query,
            'job_id': job_id,
            'processor': processor,
            'date_format': 'milli',
            'mode': mode
        }
        if df is not None:
            params['df'] = to_milli(df)
        if dt is not None:
            params['dt'] = to_milli(dt)
        return self.client.get(self.API_REPORTED_DATES, params=params)

    def delete_reported(self, series_query, reported_dates=None, delete_all=False):
        """
        Deletes reported dates.

        :param series_query: query string
        :param reported_dates: `[default: empty]` delete only specific reported dates. If not provided will delete all.
        :param delete_all: must be set to True to remove all reported dates when reported_dates is empty.
        """
        payload = {
            'series_query': series_query,
            'all': delete_all,
        }
        if reported_dates:
            payload.update({
                'date_format': 'milli',
                'reported_dates': [to_milli(dt) for dt in reported_dates],
            })
        return self.client.post(self.API_REPORTED_DATES_DELETE, data_json=payload)

    def scroll_series(self, scroll_id):
        """
        Series scroll endpoint. Retrieves the next scroll data. Should be used in tandem with
        search_series with scroll flag set to True.

        Scroll has finished when no more series are returned

        :param scroll_id: scroll id
        :return: api response
        :rtype: dict
        """
        response = self.client.get(self.API_SERIES, deserializer=options.series_serializer,
                                   params={'scroll_id': scroll_id})
        return response

    def api_status(self):
        """
        Checks Shooju API status

        :return: api response
        :rtype: dict
        """
        return self.client.get(self.API_STATUS)

    def ping(self):
        """
        Pings Shooju API

        :return: API response
        """
        return self.client.get(self.API_PING)


class Client(object):

    ALLOWED_METHODS = ('get', 'post', 'delete')  # list of allowed HTTP methods

    def __init__(self, server, user=None, password=None, base_path='/api/1',
                 retries=None, retry_delay=None, location=None, hosts=None,
                 requests_session=None, timeout=None, extra_params=None,
                 hooks=None):
        """
        REST Client

        :param str server:  url of the server including protocol ('https://alpha2.shooju.com')
        :param str user: username
        :param password: api secret
        :param retries: number of attempts to make api call
        :param retry_delay: time between api call attempts (seconds)
        :param location: Client location name
        :param hosts: Array of Shooju API endpoints. Used when access by ip, or different host name.
        :param requests_session: session object of requests.Session type to use as transport
        :param timeout: requests timeout
        :param extra_params: default url parameters that being sent to all api calls
        :param hooks: a list of API hooks
        """
        if not hosts:
            hosts = [server]
        self._headers = {'Host': six.moves.urllib.parse.urlparse(server).netloc}
        self._endpoints = cycle(['{}{}'.format(h, base_path) for h in hosts])
        self._user = user
        self._password = password

        # None means anonymous calls
        self._auth = (user, password) if all((user, password)) else None
        self._retries = retries or 3
        self._retry_delay = retry_delay or 3.
        self._location = location
        self._methods = dict()
        self._session = requests_session
        self._timeout = timeout or DEFAULT_REQUEST_TIMEOUT
        self._extra_params = extra_params or dict()
        for m in self.ALLOWED_METHODS:
            self._methods[m] = functools.partial(self._call, m)
            # copy these attributes to make it look like original function (fix functool.wraps  + sj.raw.get issues)
            self._methods[m].__module__ = self._call.__module__
            self._methods[m].__name__ = self._call.__name__
        if hooks and not all(isinstance(h, BaseHook) for h in hooks):
            raise Exception('API hook must be BaseHook subclass instance')

        self._hooks = hooks or []

    def __getattr__(self, item):
        if item not in self._methods:
            raise AttributeError('Method %s not supported' % item)
        return self._methods[item]

    def _call(self, method_name, path=None, ignore_exceptions=False, params=None,
              serializer=None, deserializer=None, deserializer_params=None, timeout=None, **kwargs):
        """
        Helper method that executes the HTTP request. By default, it json decodes the response and checks for API errors

        accepted keyword arguments:
            - binary_response (bool) flag indicating if the response is binary
            - data_json (dict) json payload
            - data_raw (str) raw payload
            - data (str) url encoded payload
            - params (dict) hash with the url parameters

        :param method_name: http method name
        :param str path: resource path
        :param kwargs: keyword arguments
        :param ignore_exceptions: if True will not check shooju exception and will return raw json response
        :param serializer: serializer instance to send data to api
        :param deserializer: serializer instance to receive data from api
        :param deserializer_params: mapping with additional response deserialization params
        :param timeout: request timeout
        :return: :raise ConnectionError: json response (or binary response if binary response selected)
        """
        serializer = serializer or options.default_serializer
        deserializer = deserializer or options.default_serializer
        deserializer_params = deserializer_params or dict()
        timeout = timeout or self._timeout
        attempt = kwargs.get('attempt', 1)
        headers, payload = dict(self._headers), None
        files = kwargs.pop('files', None)
        json_response = kwargs.get('json_response', True)
        binary_response = kwargs.get('binary_response', False)

        url = '{base}{path}'.format(base=next(self._endpoints), path=path)
        url_params = dict(self._extra_params or {})
        url_params.update(params or dict())
        url_params.update({
            'v': __version__,
            'location_type': LOCATION_TYPE,
            'location': self._location
        })

        req = Request(
            method=method_name.lower(),
            url=url,
            params=url_params,
            data_json=kwargs.get('data_json'),
            data_raw=kwargs.get('data_raw'),
            data=kwargs.get('data'),
            headers=headers,
        )
        for hook in self._hooks:
            req = hook.before_request(req)

        if req.data_json is not None:
            headers.update({'Sj-Send-Format': serializer.__name__})
            if serializer.__name__ == 'json':  # for backward compatibility
                headers.update({'content-type': 'application/json'})
            payload = serializer.dumps(req.data_json)
        elif req.data_raw:
            payload = req.data_raw
        elif req.data:
            payload = req.data

        transient_failure = False

        headers['Sj-Receive-Format'] = deserializer.__name__

        method = getattr(self._session if self._session is not None else requests, req.method.lower())
        try:
            r = method(req.url, params=req.params or None, data=payload, headers=req.headers,
                       files=files, auth=self._auth, timeout=timeout)
            if r.status_code != requests.codes.ok:
                transient_failure = r.status_code in [502, 503, 504]
                raise ConnectionError('Request failed. Error code %s' % r.status_code)
        except (requests.ConnectionError, ConnectionError, requests.Timeout) as e:
            transient_failure = transient_failure or isinstance(e, requests.ConnectionError)
            if attempt >= self._retries or not transient_failure:
                raise e
            else:
                # just a method with a full url
                request_str = '{} {}?{}'.format(
                    method_name.upper(),
                    url,
                    urlencode({k: v if v is not None else '' for k, v in (params or {}).items()})
                )
                logger.warning('failed to perform request to {}: {}. will retry in {}s'.format(
                    request_str, e, self._retry_delay))
                time.sleep(self._retry_delay)
                kwargs['attempt'] = attempt + 1
                return self._call(method_name, path, ignore_exceptions=ignore_exceptions, files=files,
                                  params=params, timeout=timeout, **kwargs)
        resp = Response(
                headers=r.headers,
                content=r.content,
                status_code=r.status_code,
                json=None if binary_response else deserializer.loads(r.content, **deserializer_params)
            )
        for hook in self._hooks:
            resp = hook.after_request(resp)

        if binary_response:
            return r
        elif json_response and not ignore_exceptions:
            return _check_errors(resp.json)
        elif json_response:
            return resp.json
        return r.text


def _check_errors(response):
    """
    Checks the API response for errors. Raises error if error is found in the response.

    :param dict response: api response
    :return: :raise ConnectionError: response
    """
    if not response['success']:
        raise ShoojuApiError(_format_error(response))
    return response


def _check_bulk_api_errors(responses):
    """
    Checks bulk API response array, if a bulk response has a series_not_found error it gets removed from the response
    :param list response: array of api responses
    :raise ConnectionError:
    """
    errors = []
    for i, response in enumerate(responses):
        if response.get('error'):
            if response['error'] == 'series_not_found':
                responses[i] = None
            else:
                errors.append(_format_error(response))

    if errors:
        raise ShoojuApiError('\n'.join(errors))


def _format_error(response):
    """
    Formats the response error
    :param response: api response
    :return: formatted error string
    """
    return '%s (%s)' % (response.get('error'), response.get('description'))


def _deseralize_points_response_directly_to_numpy(serializer):
    # small optimization for faster de-serialization if sjts is available
    if not SJTS_SUPPORTS_NUMPY or not NUMPY_INSTALLED or sjts is not options.series_serializer:
        return False
    deserialize_response_to_numpy = False
    if serializer is np_array or (PANDAS_INSTALLED and (serializer is pd_series or serializer is pd_series_localized)):
        deserialize_response_to_numpy = options.series_serializer is sjts if SJTS_INSTALLED is not None else False
    return deserialize_response_to_numpy


class BaseJob(object):
    def __init__(self, conn, job_id, batch_size, pre_hooks=None,
                 post_hooks=None, collision_retry_timeout=60, async_mode=False, skip_meta_if_no_fields=False):
        """
        Initialized with connection and job_id.

        Pre submit hooks and post commit hooks can be added to the job to perform actions before or after
        data is submitted to shooju. The function should accept kwargs

        :param shooju.Connection conn: API connection
        :param job_id: job id
        :param int batch_size: size of cache before uploading series to the API
        :param list pre_hooks: list of functions to be run before the job submits to shooju
        :param list post_hooks: list of functions to be run after the job submits to shooju
        :param int collision_retry_timeout: delay before do next attempt if series was already lock to update
        :param bool async_mode: indicates job will use async bulk requests
        :param bool skip_meta_if_no_fields: indicates that write api will not write points meta if no field written
        """
        self._conn = conn
        self._job_id = job_id
        self._batch_size = batch_size
        self._cur_batch_size = 0
        self._async_mode = async_mode
        self._skip_meta_if_no_fields = skip_meta_if_no_fields

        # those are values that will be sent to server
        # series_id will be the key and they will match to
        # {'fields':{},'points':{}} that !
        self._requests = OrderedDict()
        self._queries = OrderedDict()

        self._pre_hooks = pre_hooks or []
        self._post_hooks = post_hooks or []

        self._remove = defaultdict(lambda: {'fields': False, 'points': False})
        self._remove_query = defaultdict(lambda: {'fields': False, 'points': False})
        self._collision_retry_timeout = collision_retry_timeout

    @property
    def job_id(self):
        return self._job_id

    def finish(self, submit=True):
        """
        Optionally submits and marks a job as finished. Useful for letting all interested parties know the job is done.
        This locks the job and no further actions will be possible (writing, adding logs).

        :param submit: submit the current cached data to server before finishing job
        """
        self.submit()

    def _init_get_query_dict(self, query, delete=False, reported_date=None):
        key = query, reported_date
        if key not in self._queries:
            self._queries.setdefault(key, {})
            self._cur_batch_size += 1

        if not delete and self._queries[key].get('op') != 'post':
            self._queries[key] = {'fields': {}, 'points': {}, 'op': 'post'}
        elif delete:
            self._queries[key] = {'force': False, 'op': 'delete'}

        return self._queries[key]

    def _init_get_series_dict(self, series, delete=False, reported_date=None):
        key = series, reported_date
        if key not in self._requests:
            self._requests.setdefault(key, {})
            self._cur_batch_size += 1

        if not delete and self._requests[key].get('op') != 'post':
            self._requests[key] = {'fields': {}, 'points': {}, 'op': 'post'}
        elif delete:
            self._requests[key] = {'force': False, 'op': 'delete'}

        return self._requests[key]

    def _submit_if_bulk(self):
        """
        Submits data if we have enough bulk
        """
        if self._cur_batch_size >= self._batch_size:
            self.submit()

    def write(self, series_query, fields=None, points=None, remove_others=None):
        """
        Writes the points and/or fields to the series_query.
        The series_query must represent 0 or 1 series (writing to more than one series is not supported).
        To submit immediately, set batch_size to 1 or use submit().

        :param series_query: series query
        :param list points: list of shooju.Point
        :param dict fields: fields dict
        :param str remove_others: flag to remove all other points/points from the query.
                                  Default is None, accepts: "points", "fields" and "all"
        """
        remove_opts = {
            None: [False, False],
            'points': [True, False],
            'fields': [False, True],
            'all': [True, True],
        }
        if remove_others not in remove_opts:
            raise ValueError("remove_others should be one of None, all, points or fields")
        remove_other_points, remove_other_fields = remove_opts[remove_others]
        self._write(series_query, None, points, fields, remove_other_points, remove_other_fields)

    def write_reported(self, series_query, reported_date, fields=None, points=None):
        """
        Writes points and/or fields to the series_query and associates them with reported_date.
        The series_query must represent 0 or 1 series (writing to more than one series is not supported).
        To submit immediately, set batch_size to 1 or use submit().

        :param series_query: series query
        :param list points: list of shooju.Point
        :param dict fields: fields dict
        """
        self._write(series_query, reported_date, points, fields, False, False)

    def _write(self, series_query, reported_date, points, fields, remove_other_points, remove_other_fields):
        request = self._init_get_query_dict(series_query, reported_date=reported_date)
        if points:
            for p in points:
                request['points'].update(p.to_dict())

        if fields:
            request['fields'].update(fields)

        if remove_other_points:
            self._remove_query[series_query]['points'] = True

        if remove_other_fields:
            self._remove_query[series_query]['fields'] = True

        self._submit_if_bulk()

    def put_points(self, series_id, points):
        """
        DEPRECATED: Use write() method instead.

        Writes the points for the series_id. To submit immediately, set batch_size to 1 or use submit().

        :param series_id: series id
        :param list points: list of shooju.Point
        """
        request = self._init_get_series_dict(series_id)
        for p in points:
            request['points'].update(p.to_dict())

        self._submit_if_bulk()

    def put_reported_points(self, series_id, reported_date, points):
        """
        DEPRECATED: Use write_reported() method instead.

        Writes the points for the series_id and associates them with reported_date. To submit immediately, set batch_size to 1 or use submit().

        :param series_id: series id
        :param datetime.datetime reported_date: date reported
        :param list points: list of shooju.Point
        """
        request = self._init_get_series_dict(series_id, reported_date=reported_date)
        for p in points:
            request['points'].update(p.to_dict())

        self._submit_if_bulk()

    def put_point(self, series_id, pt):
        """
        DEPRECATED: Use write() method instead.

        Writes the point for the series_id. To submit immediately, set batch_size to 1 or use submit().

        :param shooju.Point pt: point
        :param str series_id: series id
        """
        request = self._init_get_series_dict(series_id)
        request['points'].update(pt.to_dict())

        self._submit_if_bulk()

    def put_field(self, series_id, field_name, field_value):
        """
        DEPRECATED: Use write() method instead.

        Writes the field_value under the field_name for the series_id. To submit immediately, set batch_size to 1 or use submit().

        :param str series_id: series id
        :param str field_name: name of the field
        :param str field_value: value of the field
        """

        request = self._init_get_series_dict(series_id)
        request['fields'].update({field_name: field_value})

        self._submit_if_bulk()

    def put_fields(self, series_id, fields):
        """
        DEPRECATED: Use write() method instead.

        Writes the fields for the series_id. To submit immediately, set batch_size to 1 or use submit().

        :param srt series_id: series id
        :param dict fields: fields dict
        """
        request = self._init_get_series_dict(series_id)
        request['fields'].update(fields)

        self._submit_if_bulk()

    def submit(self):
        pass

    def remove_points(self, series_id):
        """
        DEPRECATED: Use write(...remove_others="points") instead

        Sets a flag to remove all points from the series_id before the next put_point(s) call.

        :param series_id: series id to set the remove points flag
        """
        self._remove[series_id]['points'] = True

    def remove_fields(self, series_id):
        """
        DEPRECATED: Use write(...remove_others="fields") instead

        Sets a flag to remove all fields from the series_id before the next put_field(s) call.

        :param series_id: series id to set the remove fields flag
        """
        self._remove[series_id]['fields'] = True

    def add_post_submit_hook(self, fn):
        """
        Adds a hook that will be run after the cache is submitted to shooju
        :param fn: function to be executed, it should accept kwargs
        """
        self._add_hooks(self._post_hooks, fn)

    def add_pre_submit_hook(self, fn):
        """
        Adds a hook that will be run before the cache is submitted to shooju
        :param fn: function to be executed, it should accept kwargs
        """
        self._add_hooks(self._pre_hooks, fn)

    def delete(self, series_id, force=False):
        """
        DEPRECATED: Use delete_series() method instead.

        Deletes series_id.

        :param series_id: series id
        :param force: if True permanently deletes without moving to trash
        :return: True if the deletion was successful
        """
        self._init_get_series_dict(series=series_id, delete=True)['force'] = force
        self._submit_if_bulk()

    def delete_by_query(self, query, force=False):
        """
        DEPRECATED: Use delete_series() method instead.
        """
        pass

    def delete_series(self, query, one=True, force=False):
        """
        Delete series by query.

        :param query: query to base the deletion on
        :param one: True when query is a single series query
        :param force: if True permanently deletes without moving to trash
        :return: number of series deleted (moved to trash) when one is False, otherwise returns None
        """
        pass

    def delete_reported(self, series_query, reported_dates=None, delete_all=False):
        """
        Deletes reported dates.

        :param series_query: query string
        :param reported_dates: `[default: empty]` delete only specific reported dates. If not provided will delete all.
        :param delete_all: must be set to True to remove all reported dates when reported_dates is empty.
        """
        pass

    def _add_hooks(self, hook_list, fn):
        if not hasattr(fn, '__call__'):
            raise ValueError('hooks must be a function')
        hook_list.append(fn)

    def _run_pre_submit_hooks(self):
        for fn in self._pre_hooks:
            fn(job_id=self.job_id)

    def _run_post_submit_hooks(self, response):
        for fn in self._post_hooks:
            fn(job_id=self.job_id, response=response)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            return
        self.finish()
        return exc_type, exc_val, exc_tb


class RemoteJob(BaseJob):
    """
    Used to submit series points/fields to Shooju via a job id.

    Do not instantiate directly.  Use conn.register_job().
    """

    def finish(self, submit=True):
        """
        Optionally submits and marks a job as finished. Useful for letting all interested parties know the job is done.
        This locks the job and no further actions will be possible (writing, adding logs).

        :param submit: submit the current cached data to server before finishing job
        """
        super(RemoteJob, self).finish(submit=submit)
        self._conn.raw.post('/jobs/{}/finish'.format(self.job_id))

    def submit(self):
        """
        Submits the currently queued data.
        """
        # the submit part should traverse all of the sids and submit them
        self._run_pre_submit_hooks()
        bulk_data = []
        for (series, reported_date), values in self._requests.items():
            # here we will construct a BULK API call
            if values['op'] == 'delete':
                tmp_dict = {"type": "DELETE", "series_id": series, 'force': values['force']}
            else:  # post
                points = list(sorted(six.iteritems(values['points'])))
                tmp_dict = {"type": "POST", "series_id": series}
                if points:
                    tmp_dict['points'] = points
                if values['fields']:
                    tmp_dict['fields'] = values['fields']

            series_remove = self._remove.pop(series, None)

            if series_remove:
                if series_remove['points'] and series_remove['fields']:
                    remove = 'all'
                elif series_remove['points']:
                    remove = 'points'
                else:
                    remove = 'fields'
                tmp_dict['keep_only'] = remove

            if reported_date is not None:
                tmp_dict['reported_date'] = to_milli(reported_date)

            bulk_data.append(tmp_dict)

        for (query, reported_date), values in self._queries.items():
            # here we will construct a BULK API call
            if values['op'] == 'delete':
                tmp_dict = {"type": "DELETE", "query": query, 'force': values['force']}
            else:  # post
                points = list(sorted(six.iteritems(values['points'])))
                tmp_dict = {"type": "POST", "query": query}
                if points:
                    tmp_dict['points'] = points
                if values['fields']:
                    tmp_dict['fields'] = values['fields']

            query_remove = self._remove_query.pop(query, None)

            if query_remove:
                if query_remove['points'] and query_remove['fields']:
                    remove = 'all'
                elif query_remove['points']:
                    remove = 'points'
                else:
                    remove = 'fields'
                tmp_dict['keep_only'] = remove

            if reported_date is not None:
                tmp_dict['reported_date'] = to_milli(reported_date)

            bulk_data.append(tmp_dict)

        # we send the bulk data at once
        responses = []
        if bulk_data:
            try:
                responses = self._conn.shooju_api.series_write(bulk_data, job_id=self._job_id,
                                                               collision_retry_timeout=self._collision_retry_timeout,
                                                               async_mode=self._async_mode,
                                                               skip_meta_if_no_fields=self._skip_meta_if_no_fields)
            finally:
                # always flush cache
                self._requests = OrderedDict()
                self._queries = OrderedDict()
                self._cur_batch_size = 0
        self._run_post_submit_hooks({'responses': responses, 'success': True})
        return True

    def delete_by_query(self, query, force=False):
        """
        DEPRECATED: Use delete_series() method instead.

        If force==True permanently deletes all series that match the query - be careful.
        Otherwise moves these series to trash.

        :param query: query to base the deletion on
        :param force: if True permanently deletes without moving to trash
        :return: number of series deleted (moved to trash)
        """
        cnt = -1
        for cnt, r in enumerate(self._conn.scroll(query, scroll_batch_size=500)):
            self.delete(r['series_id'], force)
        self.submit()
        return cnt + 1

    def delete_series(self, query, one=True, force=False):
        """
        Delete series by query.

        :param query: query to base the deletion on
        :param one: True when query is a single series query
        :param force: if True permanently deletes without moving to trash
        :return: number of series deleted (moved to trash) when one is False, otherwise returns None
        """
        if one:
            self._init_get_query_dict(query=query, delete=True)['force'] = force
            self._submit_if_bulk()
            return

        cnt = -1
        for cnt, r in enumerate(self._conn.scroll(query, scroll_batch_size=500)):
            self._init_get_series_dict(series=r['series_id'], delete=True)['force'] = force
            self._submit_if_bulk()
        self.submit()
        return cnt + 1

    def delete_reported(self, series_query, reported_dates=None, delete_all=False):
        """
        Deletes reported dates.

        :param series_query: query string
        :param reported_dates: `[default: empty]` delete only specific reported dates. If not provided will delete all.
        :param delete_all: must be set to True to remove all reported dates when reported_dates is empty.
        """
        self._conn.shooju_api.delete_reported(series_query, reported_dates, delete_all)


class DryRunJob(BaseJob):
    POINTS_PRINT_LIMIT = 5

    def finish(self, submit=True):
        super(DryRunJob, self).finish(submit=submit)
        print('Job finished')

    def submit(self):
        for (series, reported_date), values in self._requests.items():
            if reported_date is not None:
                series = '{} @ {}'.format(series, reported_date)
            if values.get('fields'):
                print('{} fields: {}'.format(series, values['fields']))
            if values.get('points'):
                points = values['points']
                print_msg = '{} points: {}'.format(
                        series,
                        list(Point(int(d), v)
                             for d, v in values['points'].items()[:min(len(points), self.POINTS_PRINT_LIMIT)]))
                if len(points) > self.POINTS_PRINT_LIMIT:
                    print_msg += ' (only {}/{} shown)'.format(self.POINTS_PRINT_LIMIT, len(points))
                print(print_msg)
        self._remove = defaultdict(lambda: {'fields': False, 'points': False})
        self._remove_query = defaultdict(lambda: {'fields': False, 'points': False})
        self._requests = OrderedDict()
        self._queries = OrderedDict()

    def delete(self, series_id, force=False):
        print('deleted series {} with force={}'.format(series_id, force))

    def delete_by_query(self, query, force=False):
        print('deleted series by query {} with force={}'.format(query, force))


class UploaderSession(object):
    """
    DEPRECATED
    Used to upload files to Shooju via a session id.

    Do not instantiate directly.  Use conn.create_uploader_session().
    """

    def __init__(self, conn):
        """
        Initialized with connection and session_id.

        :param conn. Connection conn: API connection
        """
        self._conn = conn

    def upload_file(self, fp, filename):
        """
        Uploads a file object to Shooju. Returns the Shooju file id.

        :param fp: File Object to upload
        :param filename: Name of the file.  For cosmetic/retrieval purposes only.
        """
        return self._conn.upload_file(fp, filename)

    def init_multipart(self, filename):
        """
        Starts uploading file using multipart method. Returns the Shooju file id.

        :param filename: Name of the file.
        """
        mp = self._conn.init_multipart_upload(filename)
        return mp.file_id

    def upload_part(self, file_id, part_num, data):
        """
        Send part of file for multipart method. Returns the Shooju file id.

        :param file_id: ID assigned to the file previously.
        :param part_num: integer matching part number.
        :param data: File object or a data chunk to upload
        """
        mp = MultiPartUploader(self._conn, file_id)
        return mp.upload_part(part_num, data)

    def complete_multipart(self, file_id):
        """
        Finish upload process using multipart method. Returns the Shooju file id.

        :param file_id: ID assigned to the file previously.
        """
        mp = MultiPartUploader(self._conn, file_id)
        return mp.complete()


class MultiPartUploader(object):
    """
    Handles multi-part files upload
    """
    def __init__(self, con, file_id):
        """
        Instantiates new uploader.
        """
        self.con = con
        self.file_id = file_id

    def upload_part(self, part_num, data):
        """
        Send part of file for multipart method.

        :param part_num: integer matching part number.
        :param data: File object or a data chunk to upload
        """
        self.con.raw.post(
            '/files/multipart/upload',
            params=dict(file_id=self.file_id, part_num=part_num), files=dict(file=data)
        )

    def complete(self):
        """
        Finish upload process using multipart method. Returns the Shooju file id.

        :return: str: Uploaded file id
        """
        self.con.raw.post(
            '/files/multipart/complete',
            params=dict(file_id=self.file_id)
        )
        return self.file_id


class GetBulk(object):
    """
    That class is responsible for constructing a get bulk
    request and send it to the remote API.
    """

    def __init__(self, conn):
        """
        Gets a connection object to send the data to server
        """
        self._conn = conn
        self._reqs = []
        self._query_mode = None
        self._points_serializer_by_ix = dict()

    def get_points(self, series_id, date_start=None, date_finish=None, max_points=10,
                   size=None, serializer=None):
        """
        Long-term deprecated; get_series() using query sid="{series_id}" instead.

        Retrieves points for a series id. Can select time range. If series does not exist it returns
        None

        :param str series_id: series id
        :param datetime.datetime date_start: get points < date
        :param datetime.datetime date_finish: get points > date
                                    the historic snapshot of how the series looked after the job.
                                    (this parameter is deprecated, use @asof series operator instead)
        :param int max_points: number of points to get
        :param int size: number of points to get (this parameter is deprecated, use max_points)
        :param serializer: points serializer function; use one of shooju.points_serializers.*
        :return: points represented by `serializer` type
        :rtype: list, numpy.array, pandas.Series
        """
        self.queries_mode = False

        if size:
            max_points = size

        data = {
            '_get_type': 'get_points',
            'date_format': 'milli',
            'df': _parse_dt(date_start, 'date_start', 'MIN'),
            'dt': _parse_dt(date_finish, 'date_finish', 'MAX'),
            'max_points': max_points,
            'series_id': series_id,
        }

        self._points_serializer_by_ix[len(self._reqs)] = options.point_serializer \
            if serializer is None else serializer
        self._reqs.append(data)
        return self._ticket

    def get_fields(self, series_id, fields=None,):
        """
        Long-term deprecated; get_series() using query sid="{series_id}" instead.
        """
        self.queries_mode = False

        data = {
            '_get_type': 'get_fields',
            'series_id': series_id,
        }

        if fields:
            data['fields'] = ",".join(fields)

        self._reqs.append(data)
        return self._ticket

    def get_series(self, series_query, fields=None, df=None, dt=None, max_points=0,
                   extra_params=None, serializer=None,):
        """
        Retrieves fields and points for a series query. Can select time range. If series does not exist returns
        None

        :param str series_query: query that returns 1 series
        :param fields: list of fields to retrieve; use ['*'] for all non-meta
        :param df: date FROM for points; can be datetime(), date(), 'MAX', 'MIN', or relative date format
        :param dt: date TO for points; can be datetime(), date(), 'MAX', 'MIN', or relative date format
        :param max_points: number of points to retrieve per series; use -1 for all
        :param dict extra_params: extra parameters; refer to API Documentation
        :param serializer: points serializer function; use one of shooju.points_serializers.*
        :return: series dict with series_id and optional points and fields keys
        """
        self.queries_mode = True
        data = {
            '_get_type': 'get_points',
            'date_format': 'milli',
            'df': _parse_dt(df, 'df', 'MIN') if df is not None else None,
            'dt': _parse_dt(dt, 'dt', 'MAX') if dt is not None else None,
            'max_points': max_points,
            'query': series_query,
        }
        if extra_params:
            data.update(extra_params)

        if fields:
            data['fields'] = ",".join(fields)

        self._points_serializer_by_ix[len(self._reqs)] = options.point_serializer \
            if serializer is None else serializer
        self._reqs.append(data)

    def fetch(self):
        """
        That is the place we construct the get bulk query
        """
        # for now just puts the series id, but will change in future
        deserialize_response_to_numpy = False

        bulk_get = []
        for i, r in enumerate(self._reqs):
            request = dict(r)
            bulk_get.append(request)

            # check if we can (and should) deserialize directly to numpy array
            if not deserialize_response_to_numpy and i in self._points_serializer_by_ix:
                points_serializer = self._points_serializer_by_ix[i]
                deserialize_response_to_numpy = _deseralize_points_response_directly_to_numpy(points_serializer)

        if not bulk_get:
            return []

        deserializer_params = dict()
        if deserialize_response_to_numpy:
            deserializer_params['use_numpy'] = True

        results = self._conn.shooju_api.series_read(series_requests=bulk_get if not self.queries_mode else None,
                                                    series_queries=bulk_get if self.queries_mode else None,
                                                    deserialize_response_to_numpy=deserialize_response_to_numpy).series
        responses = []
        for i, series in enumerate(results):
            responses.append(self._process_response(self._reqs[i]['_get_type'], series, i))

        self._reqs = []
        self._query_mode = None
        self._points_serializer_by_ix.clear()

        return responses

    @property
    def queries_mode(self):
        return self._query_mode

    @queries_mode.setter
    def queries_mode(self, val):
        assert self._query_mode is None or self._query_mode == val, \
            'Can not mix series queries and series requests'

        self._query_mode = val

    def _process_response(self, get_type, series_body, index):
        """
        Converts the data from the API to Points and collects fields
        """
        if series_body is None:  # series didn't exist
            return None

        points_serializer = self._points_serializer_by_ix[index] if index in self._points_serializer_by_ix else None

        if self.queries_mode:
            if 'points' in series_body:
                series_body['points'] = points_serializer(series_body['points'],
                                                          self._conn._extract_series_tz(series_body))
            return series_body

        if get_type == "get_points":
            return points_serializer(series_body.get('points', []), tz=self._conn._extract_series_tz(series_body))
        elif get_type == "get_fields" or get_type == "get_field":
            return series_body.get('fields', {})
        elif get_type == "get_point":
            if 'points' not in series_body:
                return points_serializer([(float(self._reqs[index]['df']), None)])[0]
            pdata = series_body['points'][0]
            return points_serializer([(pdata[0], pdata[1])])[0]
        else:
            return []

    @property
    def _ticket(self):
        return len(self._reqs) - 1


def flatten(iterable):
    """
    Flattens a list

    :param iterable: list of lists
    """
    for x in iterable:
        if hasattr(x, '__iter__') and not isinstance(x, basestring):
            for y in flatten(x):
                yield y
        else:
            yield x

