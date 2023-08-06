import re
import datetime as dt

class TimeParser():
    """
    This class is used to handle time transfer of 
    time string,datetime class and timestamp,
    of course, transfer of timedelta and timedetla string 
    """
    @staticmethod
    def transfer_to(obj,to="datetime",string_formats=["%Y-%m-%d","%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M:%S.%f"],ostr_format=None):
        """
        automatic detect type of input object and transfer it to indicated type of time
        Argument:
        to: <string|datetime|timestamp>
        """
        time_datetime = None
        if isinstance(obj,str):
            for string_format in string_formats:
                try:
                    time_datetime = dt.datetime.strptime(obj,string_format)
                    break
                except:
                    pass
            if not time_datetime:
                raise Exception("input string {obj} does not match any of formats {string_formats}")
            
        elif isinstance(obj,int) or isinstance(obj,float):
            time_datetime = dt.datetime.fromtimestamp(obj)
        elif isinstance(obj,dt.datetime):
            time_datetime = obj
        
        if to == "string":
            if not ostr_format:
                ostr_format = string_format
            return time_datetime.strftime(ostr_format)
        elif to == "datetime":
            return time_datetime
        elif to == "timestamp":
            return dt.datetime.timestamp(time_datetime)
    
    @staticmethod
    def str_to_timedelta(timestr):
        """
        transfer timedelta string to timedelta class
        """
        time_format = r'((?P<days>\d+) day(s{0,1}), ){0,1}(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>[\d\.]+)'
        time_re = re.search(time_format,timestr)
        if not time_re:
            raise Exception(f"Unknown time string format {timestr}")
        else:
            days = time_re.group('days') or 0
            days = int(days)
            hours = int(time_re.group('hours'))
            minutes = int(time_re.group('minutes'))
            seconds = float(time_re.group('seconds'))
            
            return dt.timedelta(days=days,hours=hours,minutes=minutes,seconds=seconds)