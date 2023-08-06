import inspect
import warnings
import pandas as pd
import matplotlib.pyplot as plt
from functools import lru_cache
from typing import Dict, Iterable, List, Optional, Union

from holidays.constants import JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC

from holidays.constants import SAT, SUN

from datetime import date, timedelta

import holidays.countries
from holidays.holiday_base import HolidayBase


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

    :param observed: #observed는 대체공휴일 가능 나라? 인지 체크하는 거였음. TRUE or FALSE
        Whether to include the dates of when public holiday are observed
        (e.g. a holiday falling on a Sunday being observed the following
        Monday). False may not work for all countries.

    :param prov:
        *deprecated* use subdiv instead.

    :param state:
        *deprecated* use subdiv instead.

    :return: #반환값 : 해당 나라의 HolydayBase(dict) 
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

    >>> from holidays import country_holidays
    >>> us_holidays = country_holidays('US')
    # For a specific subdivision (e.g. state or province):
    >>> calif_holidays = country_holidays('US', subdiv='CA')

    The below will cause 2015 holidays to be calculated on the fly:

    >>> from datetime import date
    >>> assert date(2015, 1, 1) in us_holidays

    This will be faster because 2015 holidays are already calculated:

    >>> assert date(2015, 1, 2) not in us_holidays

    The :class:`HolidayBase` class also recognizes strings of many formats
    and numbers representing a POSIX timestamp:

    >>> assert '2014-01-01' in us_holidays
    >>> assert '1/1/2014' in us_holidays
    >>> assert 1388597445 in us_holidays

    Show the holiday's name:

    >>> us_holidays.get('2014-01-01')
    "New Year's Day"

    Check a range:

    >>> us_holidays['2014-01-01': '2014-01-03']
    [datetime.date(2014, 1, 1)]

    List all 2020 holidays:

    >>> us_holidays = country_holidays('US', years=2020)
    >>> for day in us_holidays.items():
    ...     print(day)
    (datetime.date(2020, 1, 1), "New Year's Day")
    (datetime.date(2020, 1, 20), 'Martin Luther King Jr. Day')
    (datetime.date(2020, 2, 17), "Washington's Birthday")
    (datetime.date(2020, 5, 25), 'Memorial Day')
    (datetime.date(2020, 7, 4), 'Independence Day')
    (datetime.date(2020, 7, 3), 'Independence Day (Observed)')
    (datetime.date(2020, 9, 7), 'Labor Day')
    (datetime.date(2020, 10, 12), 'Columbus Day')
    (datetime.date(2020, 11, 11), 'Veterans Day')
    (datetime.date(2020, 11, 26), 'Thanksgiving')
    (datetime.date(2020, 12, 25), 'Christmas Day')

    Some holidays are only present in parts of a country:

    >>> us_pr_holidays = country_holidays('US', subdiv='PR')
    >>> assert '2018-01-06' not in us_holidays
    >>> assert '2018-01-06' in us_pr_holidays

    Append custom holiday dates by passing one of:

    * a :class:`dict` with date/name key/value pairs (e.g.
      ``{'2010-07-10': 'My birthday!'}``),
    * a list of dates (as a :class:`datetime.date`, :class:`datetime.datetime`,
      :class:`str`, :class:`int`, or :class:`float`); ``'Holiday'`` will be
      used as a description,
    * or a single date item (of one of the types above); ``'Holiday'`` will be
      used as a description:

    >>> custom_holidays = country_holidays('US', years=2015)
    >>> custom_holidays.update({'2015-01-01': "New Year's Day"})
    >>> custom_holidays.update(['2015-07-01', '07/04/2015'])
    >>> custom_holidays.update(date(2015, 12, 25))
    >>> assert date(2015, 1, 1) in custom_holidays
    >>> assert date(2015, 1, 2) not in custom_holidays
    >>> assert '12/25/2015' in custom_holidays

    For more complex logic, like 4th Monday of January, you can inherit the
    :class:`HolidayBase` class and define your own :meth:`_populate` method.
    See documentation for examples.
    """
    try:
        country_classes = inspect.getmembers(
            holidays.countries, inspect.isclass
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


def CountryHoliday(
    country: str,
    subdiv: Optional[str] = None,
    years: Union[int, Iterable[int]] = None,
    expand: bool = True,
    observed: bool = True,
    prov: Optional[str] = None,
    state: Optional[str] = None,
) -> HolidayBase:
    """
    Deprecated name for :py:func:`country_holidays`.

    :meta private:
    """

    warnings.warn(
        "CountryHoliday is deprecated, use country_holidays instead.",
        DeprecationWarning,
    )
    return country_holidays(
        country, subdiv, years, expand, observed, prov, state
    )


def list_supported_countries() -> Dict[str, List[str]]:
    """
    Get all supported countries and their subdivisions.

    :return:
        A dictionary where the key is the ISO 3166-1 Alpha-2 country codes and
        the value is a list of supported subdivision codes.
    """
    return {
        obj.country: obj.subdivisions
        for name, obj in inspect.getmembers(
            holidays.countries, inspect.isclass
        )
        if obj.__base__ == HolidayBase
    }


def sorted_series_countries(base) :
    df = pd.Series(dict(base.items()))
    df = df.sort_index()
    return df


def count_sun(year) : #1 year
    
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


def count_sat(year) : #1 year
    
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
                 
        
def count_holidays(base, year, include_sun = False, include_sat = False) : #1 year
    
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