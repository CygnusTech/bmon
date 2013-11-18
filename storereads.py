'''
Module used to store incoming sensor readings in the database.
'''

import dateutil.parser, calendar, re, time
import bmsdata, app_settings, transforms

# open the database 
_db = bmsdata.BMSdata(app_settings.DATA_DB_FILENAME)

def store(query_params, transform_func='', transform_params=''):

    # parse the date into a datetime object and then into Unix seconds. Convert to
    # integer.
    if 'ts' in query_params:
        ts = int( calendar.timegm(dateutil.parser.parse(query_params['ts']).timetuple()) )
    else:
        # no timestamp in query parameters, so assume the timestamp is now.
        ts = int(time.time())

    # get the sensor id
    id = query_params['id']

    # Determine the final value to store
    val = query_params['val']
    if ('True' in val) or ('Closed' in val) or (val.startswith('Motion') or (val.startswith('Light'))):
        val = 1.0
    elif  ('False' in val) or ('Open' in val) or (val.startswith('No')):
        val = 0.0
    else:
        # convert to float the first decimal number
        parts = re.match(r'(-?\d+)\.?(\d+)?', val).groups('0')
        val = float( parts[0] + '.' + parts[1] )

    # if there is a transform function passed, use it to convert the reading values
    if len(transform_func.strip()):
        trans = transforms.Transformer(_db)
        ts, id, val = trans.transform_value(ts, id, val, transform_func, transform_params)

    _db.insert_reading(ts, id, val)
