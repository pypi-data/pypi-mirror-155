import datetime
from typing import Optional, Union
import re
import copy

JANELIA_GANGLIA = "cganglia.int.janelia.org/ganglia"
DEFAULT_TIMESTAMP = datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
DEFAULT_TIMEZONE = 'US/Eastern'


def extract_ip_from_link(link: str) -> Optional[str]:
    """
    Given a link with an IP address instead of a hostname,
    returns the IP (as a string).
    If the link does not contain an IP, returns None.
    Example inputs:

        http://127.0.0.1/foo
        http://10.36.111.11:38817/status
        tcp://10.36.111.11:38003
    """
    m = re.match(r'.*://(\d+\.\d+\.\d+.\d+).*', link)
    if m:
        return m.groups()[0]
    else:
        return None


def parse_timestamp(ts: Union[datetime.datetime, str], default: str = DEFAULT_TIMESTAMP, default_timezone: str = DEFAULT_TIMEZONE):
    """
    Parse the given timestamp as a datetime object.
    If it is already a datetime object, it will be returned as-is.
    If it is None, then the given default timestamp will be returned.
    If the timestamp is not yet "localized", it will be assigned a
    timezone according to the default_timezone argument.
    (That is, we assume the time in the string was recorded in the specified timezone.)
    Localized timestamps include a suffix to indicate the offset from UTC.
    See the examples below.
    Note:
        By POSIX timestamp conventions, the +/- sign of the timezone
        offset might be reversed of what you expected unless you're
        already familiar with this sort of thing.
    Example timestamps:
        2018-01-01             (date only)
        2018-01-01 00:00       (date and time)
        2018-01-01 00:00:00    (date and time with seconds)
        2018-01-01 00:00:00.0  (date and time with microseconds)
        2018-01-01 00:00-4:00  (date and time, localized with some US timezone offset)
    Returns:
        datetime
    """
    if ts is None:
        ts = copy.copy(default)

    if isinstance(ts, datetime.datetime):
        return ts
    else:
        raise ValueError('Data type not understood')

def format_ts(ts: Optional[datetime.datetime]) -> str:
    if ts is None:
        return ''
    year, month, day, hour, minute, *_ = ts.timetuple()
    return f'{month:02}/{day:02}/{year}+{hour:02}:{minute:02}'


def construct_ganglia_link(hosts: Union[List[str], str], 
                          from_timestamp, 
                          to_timestamp=None, 
                          ganglia_server=JANELIA_GANGLIA):
    if isinstance(hosts, str):
        hosts = [hosts]

    if isinstance(from_timestamp, str):
        from_timestamp = parse_timestamp(from_timestamp)

    if isinstance(to_timestamp, str):
        to_timestamp = parse_timestamp(to_timestamp)

    cs = format_ts(from_timestamp)
    ce = format_ts(to_timestamp)
    host_str = '|'.join(hosts)

    url = f'http://{ganglia_server}/?r=custom&cs={cs}&ce={ce}&m=load_one&tab=ch&vn=&hide-hf=false&hreg[]={host_str}'
    return url