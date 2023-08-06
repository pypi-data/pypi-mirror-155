from datetime import date

from dateutil.relativedelta import relativedelta as rd, MO

from holidays.constants import MON, SAT, SUN, WEEKEND #각각 0,5,6,(5,6)
from holidays.constants import (
    JAN,
    FEB,
    MAR,
    APR,
    MAY,
    JUN,
    JUL,
    AUG,
    SEP,
    OCT,
    NOV,
    DEC,
)
from holidays.holiday_base import HolidayBase
from korean_lunar_calendar import KoreanLunarCalendar
from dateutil.relativedelta import relativedelta as rd

class Korea(HolidayBase) :
    
    stat = '대체공휴일'
    enstat = ' Alternative Statutory Holiday'
    
    country = 'KR'
    
    def __init__(self, **kwargs) : 
        self.korean_cal = KoreanLunarCalendar()
        HolidayBase.__init__(self, **kwargs)
        
    def _populate(self, year) :
        
        stat = ' 대체공휴일'
        enstat =  ' Alternative Statutory Holiday'
        holi = ' 연휴'
        enholi = ' holidays'
        
        if self.en_name == True : 
            holi = enholi; stat = enstat
        
        #The first day of January
        name = '신정'
        enname = "New Year's Day"
        if self.en_name == True : 
            name = enname
                                
        self[date(year, JAN, 1)] = name
        
        if year < 1999 :
            self[date(year, JAN, 2)] = name + holi
        if year < 1990 :
            self[date(year, JAN, 3)] = name + holi
            
            
        #Korean New Year's Day
        name = '설날'
        enname = "seollal"
        if self.en_name == True : 
            name = enname
                                
        date_ = self.get_solar_date(year, 1, 1)
        seollal = date(date_.year, date_.month, date_.day)
        
        if year >= 1989 :
            self[seollal + rd(days=-1)] = name + holi
            self[seollal] = name
            self[seollal + rd(days=+1)] = name + holi
            
            if year >= 2014 and seollal.weekday() == SUN: #설날이 일요일
                self[seollal + rd(days=+2)] = name + stat
            elif year >= 2014 and seollal.weekday() == MON: #설날이 월요일
                self[seollal + rd(days=+2)] = name + stat
            elif year >= 2014 and seollal.weekday() == SAT: #설날이 토요일
                self[seollal + rd(days=+2)] = name + stat
            
        elif 1988>= year >= 1985 :
            self[date(date_.year, date_.month, date_.day)] = '민속의 날'
            if self.en_name == True :
                self[date(date_.year, date_.month, date_.day)] = 'Folkcustoms Day'
        
        
        #The March 1 Independence Movement Day
        name = '3·1절'
        enname = "The March 1 Independence Movement Day"
        if self.en_name == True : 
            name = enname
                                
        self[date(year, MAR, 1)] = name
        
        if year >= 2022 and date(year, MAR, 1).weekday() == SAT:
                self[date(year, MAR, 3)] = name+stat
        elif year >= 2022 and date(year, MAR, 1).weekday() == SUN:
                self[date(year, MAR, 2)] = name+stat
        
        #Tree Planting Day
        name = '식목일'
        enname = "Tree Planting Day"
        if self.en_name == True : 
            name = enname
                                
        if year <= 2006 :
            if year == 1960:
                self[date(year, MAR, 21)] = '사방의 날'
                if en_name == True :
                    self[date(year, MAR, 21)] = 'Tree Planting Day'            
            else :
                self[date(year, APR, 5)] = name
        
        
        #Buddha's Birthday
        name = '부처님오신날'
        name_p = '석가탄신일'
        enname = "Buddha's Birthday"
        if self.en_name == True : 
            name,name_p = enname, enname
            
                                
        date_ = self.get_solar_date(year, 4, 8)
        bud = date(date_.year, date_.month, date_.day)
        
        if year >= 2017 :
            self[bud] = name
        else :
            self[bud] = name_p
        
        
        #Children's Day
        name = '어린이날'
        enname = "Children's Day"
        if self.en_name == True : 
            name = enname  
                                
        if year >= 1975 :
            self[date(year, MAY, 5)] = name
            if year >= 2014 and date(year, MAY, 5).weekday() == SAT:
                self[date(year, MAY, 7)] = name+stat
            elif year >= 2014 and date(year, MAY, 5).weekday() == SUN:
                self[date(year, MAY, 6)] = name+stat
        
        
        #Memorial Day
        name = '현충일'
        enname = "Memorial Day"
        if self.en_name == True : 
            name = enname 
                                
        if year >= 1956 :
            self[date(year, JUN, 6)] = name
        
        
        #Constitution Day
        name = '제헌절'
        enname = "Constitution Day"
        if self.en_name == True : 
            name = enname 
                                
        if year <= 2007:
            self[date(year, JUL, 17)] = name

            
        #Liberation Day
        name = "광복절"
        enname = "Liberation Day"
        if self.en_name == True : 
            name = enname
                                
        self[date(year, AUG, 15)] = name
        
        if year >= 2021 and date(year, AUG, 15).weekday() == SAT:
                self[date(year, AUG, 17)] = name+stat
        elif year >= 2021 and date(year, AUG, 15).weekday() == SUN:
                self[date(year, AUG, 16)] = name+stat
        
        
        #Chuseok(Korean Thanksgiving Day)
        name = "추석"
        enname = "Chuseok"
        if self.en_name == True : 
            name = enname
                                
        date_ = self.get_solar_date(year, 8, 15)
        chuseok = date(date_.year, date_.month, date_.day)
        self[chuseok] = name
        
        if year >= 1986 :
            self[chuseok + rd(days=+1)] = name + holi
            
            if year >= 1989 :
                self[chuseok + rd(days=-1)] = name + holi
            
            if year >= 2014 and chuseok.weekday() == SUN:
                self[chuseok + rd(days=+2)] = name + stat
            elif year >= 2014 and chuseok.weekday() == MON:
                self[chuseok + rd(days=+2)] = name + stat
            elif year >= 2014 and chuseok.weekday() == SAT:
                self[chuseok + rd(days=+2)] = name + stat
            
            
            
        #Armed Forces Day
        name = "국군의 날"
        enname = "Armed Forces Day" 
        if self.en_name == True : 
            name = enname 
                                
        if 1976 <= year <= 1991 :
            self[date(year, OCT, 1)] = name

            
        #National Foundation Day
        name = "개천절"
        enname = "National Foundation Day"
        if self.en_name == True : 
            name = enname
                                
        self[date(year, OCT, 3)] = name
        
        if year >= 2021 and date(year, OCT, 3).weekday() == SAT:
                self[date(year,OCT,5)] = name+stat
        elif year >= 2021 and date(year, OCT, 3).weekday() == SUN:
                self[date(year,OCT,4)] = name+stat
            
            
        #Hangul Day
        name = "한글날"
        enname = "Hangul Day"
        if self.en_name == True : 
            name = enname  
                                
        if year <= 1990 or year >= 2013 :
            self[date(year, OCT, 9)] = name
            
            if year >= 2021 and date(year, OCT, 9).weekday() == SAT:
                self[date(year,OCT,11)] = name+stat
            elif year >= 2021 and date(year, OCT, 9).weekday() == SUN:
                self[date(year,OCT,10)] = name+stat
          
        
        #UN Day
        name = "유엔의 날"
        enname = "UN DAY"
        if self.en_name == True : 
            name = enname
                                
        if 1950 <= year <=1976 :
            self[date(year, OCT, 24)] = name

            
        #Christmas Day
        name = "기독탄신일" #성탄절
        enname = "Christmas"
        if self.en_name == True : 
            name = enname
                                
        self[date(year, DEC, 25)] = name

                                
        #Presidential Election
        
        enel_P = "Presidential Election"
        enel_N = "National Assembly Election"
        enel_PR = "Provincial Election"
        
        #Presidential Election
        if year == 2007:
            if self.en_name == True : self[date(year,DEC,19)] = '17th '+enel_P
            else : self[date(year,DEC,19)] = "제17대 대통령 선거일"
        elif year == 2012:
            if self.en_name == True : self[date(year,DEC,19)] = '18th '+enel_P 
            else: self[date(year,DEC,19)] = "제18대 대통령 선거일"
        elif year == 2022:
            if self.en_name == True : self[date(year,MAR,9)] = '20th '+enel_P 
            else: self[date(year,MAR,9)] = "제20대 대통령 선거일"
            
        #National Assembly Election
        if year == 2008:
            if self.en_name == True : self[date(year,APR,9)] = '18th '+enel_N
            else: self[date(year,APR,9)] = "제18대 국회의원 선거일"
        elif year == 2012:
            self[date(year,APR,11)] = "제19대 국회의원 선거일"
            if self.en_name == True : self[date(year,APR,11)] = '19th '+enel_N
        elif year == 2016:
            if self.en_name == True : self[date(year,APR,13)] = '20th '+enel_N
            else: self[date(year,APR,13)] = "제20대 국회의원 선거일"
        elif year == 2020:
            if self.en_name == True : self[date(year,APR,15)] = '21st '+enel_N
            else: self[date(year,APR,15)] = "제21대 국회의원 선거일"
            
        #Provincial Election
        if year == 2010:
            if self.en_name == True : self[date(year,JUN,2)] = '5th '+enel_PR
            else: self[date(year,JUN,2)] = "제5회 전국동시지방선거일"
        elif year == 2014:
            if self.en_name == True : self[date(year,JUN,4)] = '6th '+enel_PR
            else: self[date(year,JUN,4)] = "제6회 전국동시지방선거일"
        elif year == 2018:
            if self.en_name == True : self[date(year,JUN,13)] = '7th '+enel_PR
            else: self[date(year,JUN,13)] = "제7회 전국동시지방선거일"
        elif year == 2022:
            if self.en_name == True : self[date(year,JUN,1)] = '8th '+enel_PR
            else: self[date(year,JUN,1)] = "제8회 전국동시지방선거일"
            
            
        #Alternative Statutory Holidays 대체공휴일
        
        if year==1959:
            
            if self.en_name == True : self[date(year,APR,6)] = "Tree Planting Day Alternative Statutory Holiday"
            else: self[date(year,APR,6)] = "식목일 대체공휴일"
        elif year==1960:
           
            if self.en_name == True : 
                self[date(year,JUL,18)] = "Constitution Day Alternative Statutory Holiday"
                self[date(year,OCT,10)] = "Hangul Day Alternative Statutory Holiday"
                self[date(year,DEC,26)] = "Christmas Alternative Statutory Holiday"
            else:
                self[date(year,JUL,18)]= "제헌절 대체공휴일"
                self[date(year,OCT,10)]= "한글날 대체공휴일"
                self[date(year,DEC,26)]= "기독탄신일 대체공휴일"

        elif year==1989:
            
            if self.en_name == True : self[date(year,OCT,2)] = "Armed Forces Day Alternative Statutory Holiday"
            else :self[date(year,OCT,2)] = "국군의 날 대체공휴일"
        
        
        #Temporary Holiday 임시공휴일

        temp = ' (임시공휴일)'
        en_temp = ' (Temporary Holiday)'
        if self.en_name == True : temp = en_temp
                                
        if year==1962:
            if self.en_name == True : 
                self[date(year,APR,19)] = "Memorial Day of April 19th Revolution " + temp
                self[date(year,MAY,16)] = "Memorial Day of May 16th Revolution" + temp
                self[date(year,DEC,17)] = "Constitutional Amendment Referendum" + temp
            else:
                self[date(year,APR,19)] ="419 의거 기념일" + temp
                self[date(year,MAY,16)] ="516 혁명 기념일" + temp
                self[date(year,DEC,17)] ="헌법개정 국민투표일"+ temp
                    
        elif year ==1963:
            if self.en_name == True :   
                self[date(year,OCT,15)] = '5th '+enel_P+temp
                self[date(year,NOV,26)] = '6th '+enel_N+temp
                self[date(year,DEC,17)] = "5th Presidential Inauguration"+ temp
            else: 
                self[date(year,OCT,15)] ="제5대 대통령선거일"+ temp                     
                self[date(year,NOV,26)] ="제6대 국회의원 선거일"+ temp                    
                self[date(year,DEC,17)] ="제5대 대통령 취임일"+ temp
    
        elif year ==1965:
            if self.en_name  == True :
                self[date(year,OCT,15)] ="Sport Day"+ temp
            else:self[date(year,OCT,15)] ="체육의 날"+ temp
    
        elif year ==1967:
            if self.en_name == True :
                self[date(year,JAN,4)] = "Goverment Offices holiday"+ temp
                self[date(year,MAY,3)] = '6th '+enel_P+ temp
                self[date(year,JUN,8)] = '7th '+enel_N+ temp
                self[date(year,JUL,1)] = "6th Presidential Inauguration"+ temp
            else :
                self[date(year,JAN,4)] ="관공서 임시공휴일"+ temp
                self[date(year,MAY,3)] ="제6대 대통령 선거일"+ temp
                self[date(year,JUN,8)] ="제7대 국회의원 선거일"+ temp
                self[date(year,JUL,1)] ="제6대 대통령 취임일"+ temp
   
        elif year ==1969:
            if self.en_name == True :
                self[date(year,APR,27)] = "Apollo 11 Moon Landing Anniversary"+ temp
                self[date(year,MAY,25)] = "Constitutional Amendment Referendum" + temp
            else :
                self[date(year,APR,27)] ="아폴로 11호 달착륙 기념일"+ temp
                self[date(year,MAY,25)] ="헌법개정 국민투표일"+ temp
    
        elif year ==1971:
            if self.en_name == True : 
                self[date(year,APR,27)] = '7th '+enel_P+temp
                self[date(year,MAY,25)] = '8th '+enel_N+temp
                self[date(year,JUL,1)] = "7th Presidential Inauguration"+ temp
            else :
                self[date(year,APR,27)] ="제7대 대통령선거일"+ temp
                self[date(year,MAY,25)] ="제8대 국회의원 선거일"+ temp
                self[date(year,JUL,1)] ="제7대 대통령 취임일"+ temp
    
        elif year ==1972:
            if self.en_name == True :
                self[date(year,NOV,21)] ="Constitutional Amendment Referendum"+ temp
                self[date(year,DEC,15)] ="1st Election of representatives of the National Conference for Unification"+ temp
                self[date(year,DEC,27)] ="8th Presidential Inauguration"+ temp   
            else :
                self[date(year,NOV,21)] ="헌법개정 국민투표일"+ temp
                self[date(year,DEC,15)] ="제1대 통일주체국민회의 대의원선거일"+ temp
                self[date(year,DEC,27)] ="제8대 대통령 취임일"+ temp

        elif year ==1973:
            if self.en_name == True : 
                self[date(year,FEB,27)] = '9th '+enel_N+temp
            else : self[date(year,FEB,27)] ="제9대 국회의원 선거일"+ temp

        elif year ==1974:
            if self.en_name == True :
                 self[date(year,AUG,19)] ="State Funeral of Yuk Young-soo"+ temp
            else : self[date(year,AUG,19)] ="육영수여사 국민장일"+ temp

        elif year ==1975:
            if self.en_name == True : 
                self[date(year,FEB,12)] = "Constitutional Amendment Referendum" + temp
            else : self[date(year,FEB,12)] ="헌법개정 국민투표일"+ temp

        elif year ==1978:
            if self.en_name == True : 
                self[date(year,MAY,18)] ="2nd Election of representatives of the National Conference for Unification"+ temp
                self[date(year,DEC,12)] = '10th '+enel_N+ temp
                self[date(year,DEC,27)] = '9th '+enel_P+ temp
            else :
                self[date(year,MAY,18)] ="제2대 통일주체국민회의 대의원선거일"+ temp
                self[date(year,DEC,12)] ="제10대 국회의원 선거일"+ temp
                self[date(year,DEC,27)] ="제9대 대통령 선거일"+ temp
    
        elif year ==1979:
            if self.en_name == True :
                self[date(year,NOV,3)] ="State Funeral of President Park Chung-Hee"+ temp
                self[date(year,DEC,21)] ="10th Presidential Inauguration"+ temp               
            else : 
                self[date(year,NOV,3)] ="박정희대통령 국장일"+ temp
                self[date(year,DEC,21)] ="제10대 대통령 취임일"+ temp
    
        elif year ==1980:
            if self.en_name == True :
                self[date(year,SEP,1)] ="11th Presidential Inauguration"+ temp
                self[date(year,OCT,22)] ="Constitutional Amendment Referendum"+ temp   
            else :
                self[date(year,SEP,1)] ="제11대 대통령 취임일"+ temp
                self[date(year,OCT,22)] ="헌법개정 국민투표일"+ temp
 
        elif year ==1981:
            if self.en_name == True :
                self[date(year,FEB,11)] ="Presidential Electors Election"+ temp
                self[date(year,MAR,3)] ="12th Presidential Inauguration"+ temp
                self[date(year,MAR,25)] = '11th '+enel_N+temp    
            else: 
                self[date(year,FEB,11)] ="대통령선거인 선거일"+ temp
                self[date(year,MAR,3)] ="제12대 대통령 취임일"+ temp
                self[date(year,MAR,25)] ="제11대 국회의원 선거일"+ temp
                                
        elif year ==1982:
            if self.en_name == True :
                self[date(year,OCT,2)] ="Chuseok holiday"+ temp
            else: self[date(year,OCT,2)] ="추석 익일"+ temp

        elif year ==1985:
            if self.en_name == True : 
                self[date(year,FEB,12)] = '12th '+enel_N+temp   
            else: self[date(year,FEB,12)] ="제12대 국회의원 선거일"+ temp
    
        elif year ==1987:
            if self.en_name == True : 
                self[date(year,OCT,27)] ="Constitutional Amendment Referendum"+ temp 
                self[date(year,DEC,16)] = '13th '+enel_P+ temp
            else:
                self[date(year,OCT,27)] ="헌법개정 국민투표일"+ temp
                self[date(year,DEC,16)] ="제13대 대통령 선거일"+ temp
    
        elif year ==1988:
            if self.en_name == True : 
                self[date(year,FEB,25)] ="13th Presidential Inauguration"+ temp
                self[date(year,APR,26)] = '13th '+enel_N+temp
                self[date(year,SEP,17)] ="1988 Summer Olympics"+ temp
            else: 
                self[date(year,FEB,25)] ="제13대 대통령 취임일"+ temp
                self[date(year,APR,26)] ="제13대 국회의원 선거일"+ temp
                self[date(year,SEP,17)] ="제24회 서울올림픽 개회일"+ temp
               
    
        elif year ==1991:
            if self.en_name == True :
                self[date(year,MAR,26)] ="Basic Local Government Election"+ temp
                self[date(year,JUN,20)] ="Regional Local Government Election"+ temp
            else: 
                self[date(year,MAR,26)] ="기초자치단체 의회 의원선거일"+ temp
                self[date(year,JUN,20)] ="광역자치단체 의회 의원선거일"+ temp
                

        elif year ==1992:
            if self.en_name == True : 
                self[date(year,MAR,24)] = '14th '+enel_N+temp 
                self[date(year,DEC,18)] = '14th '+enel_P+temp
            else:
                self[date(year,MAR,24)] ="제14대 국회의원 선거일"+ temp
                self[date(year,DEC,18)] ="제14대 대통령 선거일"+ temp

        elif year ==1995:
            if self.en_name == True :
                self [date(year,JUN,27)] = '1st '+enel_PR+temp
            else: self[date(year,JUN,27)] ="제1회 전국동시지방선거일"+ temp

        elif year ==1996:
            
            if self.en_name == True : 
                self[date(year,APR,11)] = '15th '+enel_N+temp 
            else: self[date(year,APR,11)] ="제15대 국회의원 선거일"+ temp
                                
        elif year ==1997:
            if self.en_name == True : 
                self[date(year,DEC,18)] = '15th '+enel_P+temp
            else: self[date(year,DEC,18)] ="제15대 대통령 선거일"+ temp

        elif year ==1998:
            if self.en_name == True :
                self [date(year,JUN,4)] = '2nd '+enel_PR+temp
            else: self[date(year,JUN,4)] ="제2회 전국동시지방선거일"+ temp
        
        elif year ==2000:
            if self.en_name == True : 
                self[date(year,APR,13)] = '16th '+enel_N+temp
            else: self[date(year,APR,13)] ="제16대 국회의원 선거일"+ temp

        elif year ==2002:
            if self.en_name == True :
                self[date(year,JUN,13)] = '3rd '+enel_PR+temp 
                self[date(year,JUL,1)]= "2002 FIFA World Cup"+temp
                self[date(year,DEC,19)] = '16th '+enel_P+temp 
            else:
                self[date(year,JUN,13)] ="제3회 전국동시지방선거일"+ temp
                self[date(year,JUL,1)] ="2002한일월드컵경기대회"+ temp
                self[date(year,DEC,19)] ="제16대 대통령 선거일"+ temp
    
        elif year ==2004:
            if self.en_name == True : 
                self[date(year,APR,15)] = '17th '+enel_N+temp 
            else: self[date(year,APR,15)] ="제17대 국회의원 선거일"+ temp
    
        elif year ==2006:
            if self.en_name == True :
                self[date(year,MAY,31)] = '4th '+enel_PR+temp 
            else : self[date(year,MAY,31)] ="제4회 전국동시지방선거일"+ temp

        elif year ==2015:
            if self.en_name == True :
                self[date(year,AUG,14)] ="70th anniversary of Liberation Day"+ temp
            else : self[date(year,AUG,14)] ="광복절 70주년"+ temp
    
        elif year ==2016:
            if self.en_name == True : 
                self[date(year,MAY,6)] ="Children's Day Holiday"+ temp
            else: self[date(year,MAY,6)] ="어린이날 연휴"+ temp
                                
        elif year ==2017:
            if self.en_name == True :
                self[date(year,MAY,9)] = '19th '+enel_P+temp 
                self[date(year,OCT,2)] ="Chuseok Holiday"+ temp
            else :
                self[date(year,MAY,9)] ="제19대 대통령 선거일"+ temp
                self[date(year,OCT,2)] ="추석 연휴"+ temp

        elif year ==2020:
            if self.en_name == True :
                self[date(year,AUG,17)] = "Liberation Day Holiday" + temp
            else: self[date(year,AUG,17)] = "광복절 기념"+ temp
            
            
    #음력 날짜를 양력 날짜로 변환
    def get_solar_date(self, year: int, month: int, day: int) -> date:
        
        self.korean_cal.setLunarDate(year, month, day, False)
        return date(
            self.korean_cal.solarYear,
            self.korean_cal.solarMonth,
            self.korean_cal.solarDay, )
        
        
        
class KR(Korea):
    pass