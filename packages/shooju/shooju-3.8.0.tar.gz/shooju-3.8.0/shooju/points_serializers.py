from .common import *

NANOSECONDS = 1000000  # nano in milli

__all__ = [
    'shooju_point', 'milli_tuple', 'pd_series', 'pd_series_localized', 'np_array', 'Point'
]


class Point(object):
    """
    Point represents a value in the remote API
    """

    def __init__(self, dt, value, *args, **kwargs):
        """
        Representation of a point for a time series

        :param int datetime.datetime datetime.date dt: date for the point
        :param float value: value of the point
        """
        # setting job and timestamp, the trick here is that if only one of these parameters is defined it will be
        # the first element of args
        included_job = None
        included_timestamp = None
        self._job = None
        self._timestamp = None
        if 'included_job' in kwargs:
            included_job = kwargs['included_job']
        if 'included_timestamp' in kwargs:
            included_timestamp = kwargs['included_timestamp']
        if included_job and not included_timestamp:
            self._job = args[0]
        elif not included_job and included_timestamp:
            self.timestamp = args[0]
        elif included_job and included_timestamp:
            self._job, self.timestamp = args[0:2]

        self.date = dt
        self.value = value

    @property
    def job(self):
        """
        Job id
        :return: job id
        :rtype: int
        """
        return self._job

    @property
    def timestamp(self):
        """
        timestamp of the date  when the data was fetched

        :return: timestamp of the point
        :rtype: datetime.date
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        """
        Sets the timestamp of the point

        :param int float datetime.datetime datetime.date value:
        :raise ValueError:
        """
        if isinstance(value, NUMERIC_TYPES):
            self._timestamp = milli_to_datetime(value)
        elif isinstance(value, datetime):
            self._timestamp = value
        elif isinstance(value, date):
            self._timestamp = datetime(value.year, value.month, value.day)
        else:
            raise ValueError(
                '"Point" timestamp can be either millis or datetime objects only. Got "{}".'.format(type(value))
            )

    @property
    def value(self):
        """
        Value of the point

        :return: value of the point
        :rtype: float
        """
        return self._val

    @value.setter
    def value(self, value):
        """
        Sets the value of the point, only accepts float

        :param float value: value of the point
        """
        if value is not None:
            value = float(value)  # testing if it's a float
        self._val = value

    @property
    def date(self):
        """
        Date of the point

        :return: date
        :rtype: datetime.date
        """
        return date(self._dt.year, self._dt.month, self._dt.day)

    @date.setter
    def date(self, value):
        """
        Sets the date of the point

        :param int float datetime.datetime datetime.date value:
        :raise ValueError:
        """
        if isinstance(value, NUMERIC_TYPES):
            self._dt = milli_to_datetime(value)
        elif isinstance(value, datetime):
            self._dt = value
        elif isinstance(value, date):
            self._dt = datetime(value.year, value.month, value.day)
        else:
            raise ValueError(
                '"Point" date can be either millis or datetime objects only. Got "{}".'.format(type(value))
            )

    @property
    def datetime(self):
        """
        Date of the point as datetime.datetime

        :return: date of the point
        :rtype: datetime.datetime
        """
        return self._dt

    def to_dict(self):
        """
        Returns back a dictionary of the point
        which will be ready to be serialized in the
        next steps ...
        """
        return {
            to_milli(self._dt): self._val
        }

    def __repr__(self):
        return "Point(%s)" % ','.join([str(i) for i in [self._dt, self.value, self.job, self.timestamp]
                                       if i is not None])


def shooju_point(pts, *args, **kwargs):
    return [Point(*p, **kwargs) for p in pts]


def milli_tuple(pts, *args, **kwargs):
    return [tuple(p) for p in pts]


if PANDAS_INSTALLED:
    def pd_series(pts, *args, **kwargs):
        if not isinstance(pts, numpy.ndarray):
            pts = numpy.array([tuple(it) for it in pts], dtype=[('dates', 'i8'), ('values', 'f8')])
        if not len(pts):
            return pandas.Series(index=pandas.DatetimeIndex([]), data=[])
        return pandas.Series(index=pandas.DatetimeIndex(pts['dates'] * NANOSECONDS), data=pts['values'])

    def pd_series_localized(pts, tz=None, *args, **kwargs):
        from shooju.utils.convert import milli_tuple_naive_to_pandas_tz_aware
        if isinstance(pts, numpy.ndarray):
            pts = pts.tolist()
        return milli_tuple_naive_to_pandas_tz_aware(pts, tz=tz)


if NUMPY_INSTALLED:
    def np_array(pts, *args, **kwargs):
        if not isinstance(pts, numpy.ndarray):
            return numpy.array(pts)
        else:
            return pts


