# shooju

_shooju_ is the official python client library for [Shooju](http://shooju.com) with the following features:

  - Authentication via username and api key
  - Getting series points and fields
  - Registering import jobs and writing and removing points and fields

# Installation

Install with:

     pip install shooju

To install from source, use:

     python setup.py install

# Basic Usage

    >>> from shooju import Connection, sid, Point
    >>> from datetime import date
    >>> conn = Connection(server = <API_SERVER>, user = <USERNAME>, api_key = <API_KEY>)
    >>> series_id = sid("users", <USERNAME>, "china", "population")
    >>> series_query = 'sid="{}"'.format(series_id)
    >>> with conn.register_job('China Pop.') as job:
    >>>     job.write(series_query, fields={"unit": "millions"}, points=[Point(date(2012, 1, 1), 314.3)])
    >>> series = conn.get_series('sid="{}"'.format(series_id), fields=['unit'],
                                 max_points=1, df=date(2012, 1, 1), dt=date(2012, 1, 1))
    >>> print(series['points'][0].value)
    >>> print(series['fields']['unit'])

#Code samples

Code samples are in the usage_samples/ directory.  You will need to replace your user and server settings in usage_samples/sample_settings.py.

# Tutorial
## Connecting to Shooju

The first step when working with _shooju_ is to connect to Shooju using your **username** and **API key** or **google account email** and **google auth refresh token**. To authenticate with Shooju username and API key, find they api key in the accounts section of [Shooju.com](http://shooju.com)). You should also supply the server you are using:

    >>> from shooju import Connection
    >>> conn = Connection(server = API_SERVER, username = USERNAME, api_key = API_KEY)

`Connection` accepts optional `requests_session` parameter of `requests.Session` type:

    >>> import requests
    >>> session = requests.Session()
    >>> sj = Connection(API_SERVER, USERNAME, API_KEY, requests_session=session)

To retrieve the Google OAuth refresh token, follow these steps:

    >>> from shooju import Client, Connection
    >>> client = Client(API_SERVER, base_path="/api/1")
    >>> oauth_link = client.get('/auth/google_refresh_token')['link']

Open the oauth link in a web browser and copy the CODE, then use the following to retrieve the refresh token:

    >>> refresh_token = client.post('/auth/google_refresh_token', data_json={'code': CODE})['refresh_token']


## Shooju Series Representation

The basic data building block in Shooju is the **series** (i.e. time series), and each **series** is identified by a **series id**.  A **series id** is a path-like string delimited by **\\** characters.  The path helps keep data series organized into folder-like structures.  By default, each user can write into the id space **users\\your_username\\\* **.  So if I'm Sam and I want to import my GDP forecasts, I might use the series id **users\\sam\\china\\gdp**.  To help put the string together you can use a helper function like so:

    >>> from shooju import sid
    >>> series_id = sid("users","sam","china","gdp")
    >>> print(series_id)
    users\sam\china\gdp


## Writing Data

To write data, first register a **job** with Shooju:

    >>> job = conn.register_job("My description")

To write a data point onto Shooju, we first instantiate a **Point** object and specify the datetime and float value:

    >>> from datetime import date
    >>> from shooju import Point
    >>> series_id = sid("users", USERNAME, "gdp", "china")
    >>> series_query = 'sid="{}"'.format(series_id)
    >>> points = []
    >>> for i in range(1,28):
    >>>     points.append(Point(date(2010+i, 1, 1), i))
    >>> job.write(series_query, points=points)


Shooju also stores field/value data for each series.  This is commonly used to store meta-data such as source, unit, notes, etc.  To write fields into Shooju use:

    >>> job.write(series_query, fields={'source': 'Sam analysis', 'unit': 'US$bn'})

By default, **write()** call send data to Shooju immediately.  When making many **write()** calls, it is recommended to queue **write()** calls and submit them in batches.  This is done by specifying a **batch_size** when registering the job:

    >>> job = conn.register_job("another job", batch_size = 500)
    >>> series_id = sid("users", USERNAME, "gdp", "germany")
    >>> series_query = 'sid="{}"'.format(series_id)
    >>> points = []
    >>> for i in range(1,28):
    >>>     points.append(Point(date(2010+i, 1, 1), i))
    >>> job.write(series_query, fields={'source': 'My analysis', 'unit', 'US$bn'}, points=points)
    >>> job.submit() #NOTE: otherwise nothing would happen!

The job object can be used as a context manager. The below two snippets are equivalent:

    >>> job = conn.register_job("another job", batch_size = 500)
    >>> job.write(series_query, fields={'unit': 'US$bn'})
    >>> job.submit()

    >>> with conn.register_job("another job", batch_size = 500) as job:
    >>>     job.write(series_query, fields={'unit': 'US$bn'})

To delete a single series, use:

    >>> with conn.register_job("another job", batch_size = 500) as job:
    >>>     job.delete_series('sid={}'.format(series_id))

to delete many series by a query, use:

    >>> with conn.register_job("another job", batch_size = 500) as job:
    >>>     job.delete_series('sid:data', one=False)

## Getting Data

To read a single series data use **get_series()** function. The function returns a dict with `series_id`, `points` and `fields` keys. `points` and `fields` may be omitted if no points/fields were returned.
By default the function does not fetch points/fields.

To get an array of points pass the following parameters: `df` (date from), `dt` (date to) and `max_points`.  Note that `df` and `dt` arguments are optional, but `max_points` is required when fetching points because the default value is 0:

    >>> from datetime import date
    >>> series = conn.get_series(u'sid="{}"'.format(series_id), df=date(2011,1,1), dt=date(2020,1,1), max_points=-1)
    >>> print(series['points'][0].date, ser['points'][0].value)
    2012-01-01 00:00:00 1.0

As noted above get_series() doesn't fetch points by default. To fetch points explicitly set `max_points` (must be integer greater than 0). To fetch ALL points set `max_points` to a special value `-1`:

    >>> print(conn.get_series(u'sid="{}"'.format(series_id), df=date(2011,1,1), max_points=1)['points'].value)
    1.0

To get field values, use:

    >>> print(conn.get_series('sid="{}".format(series_id), fields=["unit"]))['fields']['unit']
    US$bn


To get all of the fields for a given series pass '*' in the `fields` parameter:

    >>> print conn.get_series(u'sid="{}"'.format(series_id), fields=['*'])['points']['fields']
    {"unit":"US$bn", "source":"usa"}

To get some of the fields under given series, use:

    >>> print conn.get_fields(u'sid="{}"'.format(series_id), fields=["source"])
    {"unit":"US$bn"}

## Getting multiple data at once (multi-get)

By default, each **get_series()** call makes one blocking API request.  If we were to make all the calls in the getting data example above, we would be making 5 API calls.  Shooju API supports multiple get requests via the BULK API, which is much more efficient if we intend to make multiple requests.

To initialize a muti-get request:

    >>> mget = conn.mget()

Now we can use **get_series()*** function.  Keep in mind that the function does not return the data, but instead queues the requests for fetching.  We can reproduce the **get_series()*** requests introduced above:

    >>> series_query = u'sid="{}"'.format(series_id)
    >>> mget.get_series(series_query, df=date(2011,1,1), dt=date(2020,1,1), max_points=-1)
    0
    >>> mget.get_series(series_query, df=date(2011,1,1), max_points=1)
    1
    >>> mget.get_series(series_query, fields=["unit"])
    2
    >>> mget.get_series(series_query, fields=["*""])
    3
    >>> mget.get_fields(series_query, fields=["source"])
    4

To get an array containing the results in the order that the **get\_\*** requests were called:

    >>> result = mget.fetch()
    >>> print result[2]['fields']
    US$bn

## Scroll

To fetch a big number of series by a given query use `scroll()`. This function accepts the same points/fields related parameters as `get_series()`:

    >>> for s in conn.scroll('sid:users\\me', fields=['unit'], max_points=-1, df=date(2001, 1, 1)):
    >>>     print('sid: {} points: {} fields: {}'.format(s['series_id'], s.get('points'), s.get('fields')))


## Points serializers

By default `get_series` and `scroll` return points represented as a list of `shooju.Point` objects. This behaviour can be changed by using `shooju.points_serializers`.

    >>> from shooju import points_serializers as ps
    >>> ser = conn.get_series(u'sid="{}"'.format(series_id), max_points=-1, serializer=ps.pd_series)
    >>> print(ser['points'])
    1980-01-01    12.0
    dtype: float64

Supported serializers:

- `milli_tuple` - an array of date milli and value tuples.
- `pd_series` - pandas.Series where date represented as `DatetimeIndex`.
- `pd_series_localized` - the same is above but `DatetimeIndex` is localized if `@localize` operator was used.
- `np_array` - a Numpy array.

## Generating a pandas.DataFrame from Shooju series data (get_df)

To generate a pandas.DataFrame from series query use `get_df()`. This function has a private parameter `series_axis`, which is used to set series position on DataFrame - the default `rows` or `columns`. Beside that, `get_df()` accepts the same points/fields related parameters as `get_series()` and `scroll()`.

Generates pandas.DataFrame with fields as columns and series as rows.

    >>> df = conn.get_df('sid:users\\me', fields=['*'])
    >>> print(df)
        series_id          unit      description
    0   users\me\unit-a    unit A    Unit A
    1   users\me\unit-b    unit B    Unit B
    3   users\me\unit-c    unit C    Unit C
    ...

 To generate DataFrame with series values as columns and points as rows, pass the parameter `series_axis='columns'`. If specific fields are passed, the values will define the DataFrame indexes joined by the character `'/'`.

    >>> df = conn.get_df('sid:users\\me', fields=['unit', 'description'], series_axis='columns', max_points=-1)
    >>> print(df)
                 unit A/Unit A    unit B/Unit B   ...    unit Z/Unit Z
    2000-04-03   20.50            31.50           ...    34.20
    2000-04-04   32.25            20.50           ...    36.00
    2000-04-05   31.25            40.50           ...    46.50
    ...

`get_df()` always returns localized DataFrame. By default it's in UTC, but if `@localized:<tz>` operator applied, it will be in `<tz>`. To convert DataFrame's index to naive use `df.tz_localize(None)`.

## REST Client

To use other APIs, use the configured REST client in Connection:

    >>> from shooju import Connection
    >>> conn = Connection(username = USERNAME, api_key = API_KEY, server = API_SERVER)
    >>> conn.raw.get('/teams')
    >>> conn.raw.post('/teams/myteam/', data_json={'description': 'my description'})

To send url parameters, use the `params` argument:

    >>> conn.raw.get('/series', params={'series_id': r'user\series\s1'}


## Change log

**3.8.0**

- Added support of low level API hooks

**3.7.0**

- New attributes `Point.timestamp` and `Point.job`

**3.6.0**

- BREAKING CHANGE: Columns of`pandas.DataFrame` that `Connection.get_df()` returns were renamed from `points` and `date` to `val` and `dt` 
- Reduced `Connection.get_df()` memory footprint
- `Connection.get_df()` omits rows where points values are nan

**3.5.1**

- new `custom_fields` parameter in Connection.upload_file()

**3.5.0**

- introduce Connection.upload_file() and Connection.init_multipart_upload() methods
- deprecate Connection.create_uploader_session() and UploaderSession()
- job.delete_reported() to delete certain reported dates


**3.4.3**

- Fix exception in `Connection.get_df()` due to mixing naive and localized pandas.Series().

**3.4.2**

- Global extra_params was ignored in Connection.raw calls.

**3.4.1**

- Minor internal changes. Stopped using the derprecated parameters of /series/write endpoint.
- Fix Connection.get_df() error when scrolling over series with no points.

**3.4.0**

- New `options.return_series_errors` to control how series level errors are handled

**3.3.1**

- `Connection` accepts new `extra_params` parameter

**3.3.0**

- `RemoteJob.delete()` and `RemoteJob.delete_by_query()` are now deprecated. Use `RemoteJob.delete_series()`.

**3.2.0**

- `Connection.get_df()` now always returns localized DataFrame

**3.1.0**

- Added multipart upload for huge files

**3.0.3**

- Fixed ability to make anonymous calls against public endpoints

**3.0.2**

- Fixed Python 2 compatibility issues

**3.0.1**

- Minor internal refactoring

**3.0.0**

- New `Connection.get_df()` function to generate a pandas.DataFrame from Shooju series data
- Removed deprecated Connection.get_point()/get_field() and GetBulk.get_point()/get_field()
- Removed the following deprecated parameters from read functions: snapshot_job_id, snapshot_date, reported_date, operators, date_start, date_finish

**2.3.0**

- Added RemoteJob(skip_meta_if_no_fields=...) parameter

**2.2.0**

- `Connection.search()` been deprecated and now removed.
- Added `timeout` parameter to Connection. This controls HTTP requests timeout.

**2.1.1**

- Fix compatibility issues with the most recent msgpack version.


**2.1.0**

- Deprecate put_* job methods. The new write()/write_reported() methods introduced as a replacement.


**2.0.16**

- Improve date parse error message


**2.0.15**

- Connection(...proxies={...}) parameter has been replaced by Connection(...requests_session=requests.Session()) in favor of better flexibility


**2.0.14**

- added proxies support

**2.0.13**

- fixed error when writing points with tz-aware dates

**2.0.12**

- added ability to define direct IPs of API servers

**2.0.11**

- fixed milliseconds being cut-off on points write

**2.0.10**

- pd_series points serializer fix

**2.0.9**

- Stopped using Pandas deprecated feature

**2.0.8**

- Minor request retry logic improvements

**2.0.7**

- Deprecate `snapshot_job_id`, `snapshot_date` and `reported_date` parameters. `@asof` and `@repdate` must be used instead.
- get_series() accepts `operators` parameter
- Added `pd_series_localized` points serializer

**2.0.6**

- Fix Python 3.7 compatibility.

**2.0.5**

- Edge case fix. Wasn't able to wrap sj.raw.<method> with functools.wraps.

**2.0.4**

- Fixed thread safety bug.
- New optional "location" Connection() parameter to identify the application that using the API.

**2.0.3**

- Breaking change: the first parameter of Connection.get_reported_dates() is now series_query.  It was series_id before.  To convert from series_id to series_query, remove the $ from the beginning or prepend sid="<series_id>".

**2.0.2**

- Log warning on request retry.

**2.0.1**

- Bug fixes.

**2.0.0**

- Added preferred new get_series() method.
- Moved writes to SJTS format for serialization and transport.
- Allowed relative date format in df / dt parameters.
- Big changes in scroll():
  - date_start -> df  (date_start still works but will be removed in future versions)
  - date_finish -> dt (date_finish still works but will be removed in future versions)
  - removed deprecated parameters: query_size, sort_on, sort_order, size
  - added max_series
  - added extra_params
- Deprecated get_point and get_field methods.  These will be removed in future versions.
- Deprecated search method in favor of scroll.  It will be removed in future versions.

**0.9.7**

- Python 3 compatibility fixes.

**0.9.6**

- Points serializers bug fixes.

**0.9.5**

- Added operators parameter in the pd.search() function.
- Added reported_date parameter to the get_points() functions.
- Added job.put_reported_points(series_id, reported_date, points) to write reported points based on a date.
- Added get_reported_dates(series_id=None, job_id=None, processor=None, df=None, dt=None) to retrieve all reported_dates for one of: series_id, job_id, processor.
- Added snapshot_date and snapshot_job_id to all get_points() functions.
- Added serializer parameter to all get_points() functions.  Built-in options are under shooju.points_serializers.*.  The default can be set using shooju.options.point_serializer = shooju.points_serializers.pd_series.
- Removed pd.get_points() and pd.get_fields().  Use serializer=shooju.points_serializers.pd_series instead.

**0.9.1**

- Fixed negative epoch times (before year 1970) on non-unix.
- Now using DatetimeIndex in pandas formatter for faster pandas dataframe serialization.
- Removed pd.get_points and pd.get_fields functions.  Use pd.search() instead.
- Now applying options.point_serializer everywhere. (edited)

**0.9.0**

- Job.delete() is now part of bulk request. Use Job.submit() to run immediately.
- Connection.delete() and Connection.delete_by_query() have been removed. Use the equivalents in job instead.

**0.8.5**

- Fixed mget().get_point() bug.

**0.8.4**

- Bug fixes.

**0.8.3**

- SJTS bug fixes.

**0.8.2**

- Bug fixes and json/msgpack/sjts auto support.

**0.8.1**

- Bug fixes.

**0.8.0**

- Removed ujson.
- Using new /series API.
- Changed size to max_points parameter.  Size is still supported, but switching to max_points is encouraged.

**0.7.8**

- Optional ujson.
- Added options.point_serializer (shooju_point / milli_tuple).

**0.7.7**

- Bug fixes.

**0.7.6**

- Added options.sjts_stream.

**0.7.5**

- Added options.sjts_chunk_size.
- Do not fetch fields when not necessary.

**0.7.4**

- Added SJTS.
- Moved internal dates from unix to milli.

**0.7.3**

- Added internal async.

**0.7.2**

- Bug fixes.

**0.7.1**

- Series are now written in the order of put\_* calls.
- Added retry on lock failures.

**0.7.0**

- Retry on temporary API failure.
- Added reported_group concept.
- Added support for Python 3.

**0.6.2**

- Add operators parameter to scroll and search functions.  To use, pass in an array of operators without the @.  For example, operators = ['MA'].


**0.6.1**

- Ability to upload files using sess = conn.create_uploader_session() and sess.upload_file()
- conn.get_points(), get_point(), get_field() and get_fields() now accept snapshot_job_id and snapshot_date parameters. These parameters allow fetching historic snapshots of how the series looked after the job or at specific datetime.


**0.6.0**

- BREAKING CHANGE: search() now returns a list instead of a dictionary.
- search() and scroll() now accept sort_on and sort_order paramters.
- If a non-url string is provided to Connection(), https://{}.shooju.com will be attempted.
- Simpler OAuth interface and instructions have been added.  See bitbucket page for details.
- Added force parameter to delete_by_query.

**0.5.0**

- Added job.finish(submit=True) to submit job buffer and mark a job as finished.
- Added job context to be used like: with connection.register_job('testjob') as job: ...

**0.4.8**

- Added email and google_oauth_token kwargs to Connection() to allow authentication through Google Oauth.  Environment variables SHOOJU_EMAIL and SHOOJU_GOOGLE_OAUTH_TOKEN can be used instead of parameters.
- Added Connection.user property to find the currently logged in user.

**0.4.7**

- Bug fixes.

**0.4.6**

- Added delete_by_query function.
- Exposed query_size in scroll().
- Changed default size from 10 to 0 in scroll().

**0.4.5**

- Added remove_points and remove_fields methods to RemoteJob to clear the fields/points before sending new data.

**0.4.4**

- Change Connection search default point size to 0

**0.4.3**

- Fix another job cache error.

**0.4.2**

- Added pre and post submit hooks to RemoteJob to perform actions after submitting a job to shooju


**0.4.1**

- Fix job cache error, if exception was raised cache was not flushed

**0.4**

- Connection().pd.search_series renamed to search
- Change way DataFrame is formatted when using Connection().pd.search()
- Added key_field parameters to Connection().pd.search() to add a custom name for the column using series fields

**0.3**

- Connection().scroll() fixed
- Initializing Connection doesn't ping the API
- If series does not exist get_point, get_points, get_field, get_fields return None

**0.2**

- Connection().multi_get() renamed to mget()
- mget().get_points(), get_fields(), get_point() and get_field() return index of their result
- Connection().register_job() requires a description of more than 3 chars
- Connection().scroll_series() renamed to scroll()
- Renamed and rearranged Connection parameters: Connection(server, user, api_key)
- Field object removed, fields return a simple dict
- Points can have value of None