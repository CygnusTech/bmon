'''
Utilities used in the data analysis used to produce data for charts and reports.
'''

from datetime import datetime
import pytz, calendar, time, math
from dateutil import parser
import numpy as np
from django.conf import settings


# Default timezone used when a datetime value needs to be created
default_tz = pytz.timezone(getattr(settings, 'TIME_ZONE', 'US/Alaska'))

def ts_to_datetime(unix_ts=time.time(), tz=default_tz):
    '''
    Converts a UNIX timestamp (seconds) to a Python datetime object in a
    particular timezone.  The timezone info is stripped from the returned
    datetime to make it naive, which works better with the Pandas library
    '''
    return datetime.fromtimestamp(unix_ts, tz).replace(tzinfo=None)

def datestr_to_ts(datestr, tz=default_tz):
    '''
    Converts a date/time string into a Unix timestamp, assuming the date/time is expressed
    in the timezone 'tz'.
    '''
    dt = parser.parse(datestr)
    dt_aware = tz.localize(dt)
    return calendar.timegm(dt_aware.utctimetuple())

def round4(val):
    '''
    Rounds a number to a 4 significant digits, unless it is an integer.
    '''
    if val != int(val):
        return float('%.4g' % val)
    else:
        return val

def decimals_needed(vals, sig_figures):
    '''Returns the number of digits past the decimal needed to ensure
    that 'sig_figures' significant figures are displayed for the largest
    value (in absolute value terms) in the array of values 'vals'. 
    '''
    if len(vals):
        max_val = max(abs(min(vals)), abs(max(vals)))
        if max_val != 0:
            return max(0, sig_figures - int(math.log10(max_val)) - 1)
        else:
            return 0
    else:
        # No values in the array, just return 0.
        return 0

def formatCurVal(val):
    """
    Helper function for formatting current values to 3 significant digits, but 
    avoiding the use of scientific notation for display.  Also, integers are
    shown at full precision.
    """
    if val == int(val):
        return '{:,}'.format(int(val))
    elif val >= 1000.0:
        return '{:,}'.format( int(float('%.3g' % val)))
    else:
        return '%.3g' % val


class TsBin:
    '''
    Class to determine a timestamp bin value (UNIX seconds) for purposes of time-averaging
    data.  Bins are aligned to the start of a Monday, standard time, in the requested timezone.
    No accounting of daylight savings time occurs for establishment of the bins.
    '''

    def __init__(self, bin_width, tz=default_tz):
        '''
        'bin_width' is the bin width in hours.  The values of 720 and 8760 are
        treated special.  The value 720 indicates that binning by month is
        requested, and actual month boundaries are used to determine the bins
        instead of bins exactly 720 hours wide.  A value of 8760 indicates
        that yearly bins are requested, and bins will be on exactly year
        boundaries instead of exactly 8760 hours wide.
        '''

        # save bin width in hours and in seconds
        self.bin_width = bin_width
        self.bin_wid_secs = bin_width * 3600.0  # bin width in seconds

        self.tz = tz  # save timezone

        # determine a reference timestamp that occurs at the start of a bin boundary for all
        # binning widths.  That would be a Monday at 0:00 am.
        ref_dt = tz.localize(datetime(2000, 1, 3))
        self.ref_ts = calendar.timegm(ref_dt.utctimetuple())

    def bin(self, ts):
        '''
        Returns the bin midpoint for 'ts' in Unix seconds.

        Month and Year binning are slow (~17 us per timestamp) and could be sped
        up by creating a dictionary that maps each day to a bin timestamp.  The
        dictionary keys would span a range of all likely timestamps and would be
        created in the __init__ constructor. The timestamp passed into this bin
        routine would first be moved to the start of the day to conform with the
        dictionary keys.
        '''
        if self.bin_width == 720:
            # month binning. Put it into bin in middle of month.
            dt = datetime.fromtimestamp(ts, self.tz).replace(day=16, hour=0, minute=0, second=0, microsecond=0)
            # this may still be expressed in Standard time instead of Daylight Savings time, so correct
            dt = self.tz.normalize(dt).replace(hour=0)
            return calendar.timegm(dt.utctimetuple())

        if self.bin_width == 8760:
            # year binning.  Bin is middle of year (roughly)
            dt = datetime.fromtimestamp(ts, self.tz).replace(month=7, day=1, hour=0, minute=0, second=0, microsecond=0)
            # this may still be expressed in Standard time instead of Daylight Savings time, so correct
            dt = self.tz.normalize(dt).replace(hour=0)
            return calendar.timegm(dt.utctimetuple())

        else:
            bin_int = int((ts - self.ref_ts) / self.bin_wid_secs)
            return bin_int * self.bin_wid_secs + self.bin_wid_secs * 0.5 + self.ref_ts


def histogram_from_series(pandas_series):
    '''
    Returns a list of histogram bins ( [bin center point, count] ) for the Pandas
    Time Series 'pandas_series'.  The values of the series (index not involved) are used
    to create the histogram.  The histogram has 30 bins.
    '''

    cts, bins = np.histogram(pandas_series.values, 20)   # 20 bin histogram
    avg_bins = (bins[:-1] + bins[1:]) / 2.0       # calculate midpoint of bins

    # round these values for better display in Highcharts
    avg_bins = [round4(x) for x in avg_bins]

    # Convert count bins into % of total reading count
    reading_ct = float(sum(cts))
    cts = cts.astype('float64') / reading_ct * 100.0
    cts = [round4(x) for x in cts]

    # weirdly, some integer are "not JSON serializable".  Had to 
    # convert counts to float to avoid the error.  Also, round bin average
    # to 4 significant figures
    return zip(avg_bins, cts)
