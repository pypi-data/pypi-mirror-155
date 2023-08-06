import inspect
import warnings
import pandas as pd
import matplotlib.pyplot as plt
from functools import lru_cache
from typing import Dict, Iterable, List, Optional, Union

from krholidays.constants import JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC

from krholidays.constants import SAT, SUN

from datetime import date, timedelta

import krholidays.countries
from krholidays.holiday_base import HolidayBase


def country_holidays(
    country: str,
    subdiv: Optional[str] = None,
    years: Union[int, Iterable[int]] = None,
    expand: bool = True,
    observed: bool = True,
    prov: Optional[str] = None,
    state: Optional[str] = None,
    en_name : bool = False
    
) -> HolidayBase:
    """
    Returns a new dictionary-like :py:class:`HolidayBase` object for the public
    holidays of the country matching **country** and other keyword arguments.

    :param country:
        An ISO 3166-1 Alpha-2 country code.

    :param subdiv:
        The subdivision (e.g. state or province); not implemented for all
        countries (see documentation).

    :param years:
        The year(s) to pre-calculate public holidays for at instantiation.

    :param expand:
        Whether the entire year is calculated when one date from that year
        is requested.

    :param observed: 
        Whether to include the dates of when public holiday are observed
        (e.g. a holiday falling on a Sunday being observed the following
        Monday). False may not work for all countries.

    :param prov:
        *deprecated* use subdiv instead.

    :param state:
        *deprecated* use subdiv instead.

    :return: #반환값 : 해당 나라의 HolidayBase(dict) 
        A :py:class:`HolidayBase` object matching the **country**.

    The key of the :class:`dict`-like :class:`HolidayBase` object is the
    `date` of the holiday, and the value is the name of the holiday itself.
    Dates where a key is not present are not public holidays (or, if
    **observed** is False, days when a public holiday is observed).

    When passing the `date` as a key, the `date` can be expressed in one of the
    following types:

    * :class:`datetime.date`,
    * :class:`datetime.datetime`,
    * a :class:`str` of any format recognized by :func:`dateutil.parser.parse`,
    * or a :class:`float` or :class:`int` representing a POSIX timestamp.

    The key is always returned as a :class:`datetime.date` object.

    To maximize speed, the list of public holidays is built on the fly as
    needed, one calendar year at a time. When the object is instantiated
    without a **years** parameter, it is empty, but, unless **expand** is set
    to False, as soon as a key is accessed the class will calculate that entire
    year's list of holidays and set the keys with them.

    If you need to list the holidays as opposed to querying individual dates,
    instantiate the class with the **years** parameter.

    Example usage:

    >>> from krholidays import country_holidays
    >>> kr = country_holidays('KR')


    Append custom holiday dates by passing one of:

    * a :class:`dict` with date/name key/value pairs (e.g.
      ``{'2010-07-10': 'My birthday!'}``),
    * a list of dates (as a :class:`datetime.date`, :class:`datetime.datetime`,
      :class:`str`, :class:`int`, or :class:`float`); ``'Holiday'`` will be
      used as a description,
    * or a single date item (of one of the types above); ``'Holiday'`` will be
      used as a description:

    >>> custom_holidays = country_holidays('KR', years=2015)
    >>> custom_holidays.update({'2015-01-01': "New Year's Day"})
    >>> custom_holidays.update(['2015-07-01', '07/04/2015'])
    >>> custom_holidays.update(date(2015, 12, 25))
    >>> assert date(2015, 1, 1) in custom_holidays
    >>> assert date(2015, 1, 2) not in custom_holidays
    >>> assert '12/25/2015' in custom_holidays

    For more complex logic, like 4th Monday of January, you can inherit the
    :class:`HolidayBase` class and define your own :meth:`_populate` method.
    """
    try:
        country_classes = inspect.getmembers(
            krholidays.countries, inspect.isclass
        )
        country_class = next(
            obj for name, obj in country_classes if name == country
        )
        country_holiday = country_class(
            years=years,
            subdiv=subdiv,
            expand=expand,
            observed=observed,
            prov=prov,
            state=state,
            en_name = en_name
        )
    except StopIteration:
        raise NotImplementedError(f"Country {country} not available")
    return country_holiday


def count_sun(year) : #on a yearly basis
    
    sun_num = 0
    sun_date = []
    
    for month in range(1,13) :
        if month in [JAN, MAR, MAY, JUL, AUG, OCT, DEC] :
            for day in range(1,32) :
                if date(year,month,day).weekday() == SUN :
                    sun_num = sun_num + 1
                    sun_date.append(date(year,month,day))
        elif month == 2 :
            if ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0): 
                for day in range(1,30) :
                    if date(year,month,day).weekday() == SUN :
                        sun_num = sun_num + 1
                        sun_date.append(date(year,month,day))
            else :
                for day in range(1,29) :
                    if date(year,month,day).weekday() == SUN :
                        sun_num = sun_num + 1
                        sun_date.append(date(year,month,day))
        else :
            for day in range(1,31) :
                if date(year,month,day).weekday() == SUN :
                    sun_num = sun_num + 1
                    sun_date.append(date(year,month,day))
                    
                    
    return sun_num, sun_date


def count_sat(year) : #on a yearly basis
    
    sat_num = 0
    sat_date = []
    
    for month in range(1,13) :
        if month in [JAN, MAR, MAY, JUL, AUG, OCT, DEC] :
            for day in range(1,32) :
                if date(year,month,day).weekday() == SAT :
                    sat_num = sat_num + 1
                    sat_date.append(date(year,month,day))
        elif month == 2 :
            if ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0): 
                for day in range(1,30) :
                    if date(year,month,day).weekday() == SAT :
                        sat_num = sat_num + 1
                        sat_date.append(date(year,month,day))
            else :
                for day in range(1,29) :
                    if date(year,month,day).weekday() == SAT :
                        sat_num = sat_num + 1
                        sat_date.append(date(year,month,day))
        else :
            for day in range(1,31) :
                if date(year,month,day).weekday() == SAT :
                    sat_num = sat_num + 1
                    sat_date.append(date(year,month,day))
                    
                    
    return sat_num, sat_date
                 
        
def count_holidays(base, year, include_sun = False, include_sat = False) : #on a yearly basis
    
    holiday_num, holiday_date = len(base), list(base.keys())
    
    if include_sun == True :
        
        sum_num, sun_date = count_sun(year)
        
        if include_sat == True :
            
            sat_num, sat_date = count_sat(year)
            net_holiday_date = list(set(holiday_date+sat_date+sun_date))
            net_holiday_num = len(net_holiday_date)
            
            return net_holiday_num
            
        net_holiday_date = list(set(holiday_date+sun_date))
        net_holiday_num = len(net_holiday_date)
        
        return net_holiday_num

    else :
        return holiday_num
    

#def workdays(base, year) :
#    
#    if year>=2005 :
#        return 365-(count_holidays(base,year,include_sun = True, include_sat = True)+1)
    
#    elif year >= 1958 :
#        return 365 - (count_holidays(base,year,include_sun = True)+1)
    
#    else :
#        return 365 - count_holidays(base,year,include_sun = True)
    


def years_graph(start, end, sat = False, sun = False) :
    
    years = list(range(start,end+1)) #x축
    num = [] #y축

    for year in range(start,end+1) :
        temp = count_holidays(country_holidays('Korea',years = year),year, include_sat = sat, include_sun = sun)
        num.append(temp)
                          
    plt.figure(figsize= (20,12))
    plt.bar(x = years, height = num, color = '#FF92FD')
    plt.ylim((60,72))
    plt.show()
    

def months_graph(year) :
    years = list(range(1,13)) #x축
    num = [] #y축

    month_last = {1 : 31, 2 : 28, 3 : 31, 4 : 30, 5 : 31, 6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31, 11 : 30, 12 : 31}

    for month in range(1,13) :
        temp = len(country_holidays('Korea',years = year)[date(year,month,1):date(year,month,month_last[month])])
        num.append(temp)
                          
    plt.figure(figsize= (20,12))
    plt.bar(x = years, height = num, color = '#B0BF1A')
    plt.title('Korean Holidays in {}'.format(year), fontsize = 20)
    plt.show()