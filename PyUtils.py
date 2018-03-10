
import os
#import cx_Oracle as ora
import datetime
from dateutil import rrule

def resource_path(relative):
    return os.path.join(
        os.environ.get(
            "_MEIPASS2",
            os.path.abspath(".")
        ),
        relative
    )
        
# Get Date String as YYYYMMDD (business day)
def GetDateStr(days_before=0):
    #holidays = [
    #datetime.datetime(2016, 12, 6,),
    #datetime.datetime(2016, 12, 7,),
    ## ...
    #]
#    holidays_file = 'holidays.txt'

    if (os.path.isfile(resource_path('holidays.txt')) == False):
        print('Not exists holidays.txt with exe file')
        
        today = datetime.date.today() - datetime.timedelta(days=days_before)
        yesterday = today - datetime.timedelta(days=1)
        
        while(yesterday.weekday() in [5, 6]):
            yesterday -= datetime.timedelta(days=1)
        
        today_str = today.strftime('%Y%m%d')
        yesterday_str = yesterday.strftime('%Y%m%d')        

        return yesterday_str, today_str
    else:
        f = open(resource_path('holidays.txt'), 'r')
        dates = f.read().splitlines()
        holidays = [datetime.datetime.strptime(date, '%Y%m%d') for date in dates]

        # Create a rule to recur every weekday starting today
        r = rrule.rrule(rrule.DAILY,
                        byweekday=[rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR],
                        dtstart=datetime.date.today()-datetime.timedelta(30),until=datetime.date.today()-datetime.timedelta(days_before))

        # Create a rruleset
        rs = rrule.rruleset()

        # Attach our rrule to it
        rs.rrule(r)

        # Add holidays as exclusion days
        for exdate in holidays:
            rs.exdate(exdate)

#        yesterday = max(rs[:])
#        today = datetime.date.today() - datetime.timedelta(days=days_before)

        yesterday = rs[-2]
        today = rs[-1]

        yesterday_str = yesterday.strftime('%Y%m%d')
        today_str = today.strftime('%Y%m%d') 

        return yesterday_str, today_str

# For DB Table linking..
def query_linker(input_str):
    import DB_NAME
    str_A = DB_NAME.A
    str_B = DB_NAME.B
    
    out_str = input_str
        
    for key in str_A+str_B:
        out_str = out_str.replace(key, key+"@")
        
    return out_str


if __name__ == '__main__':
#    test_dsn = ora.makedsn('ip', port, name)
#    conn = ora.connect(id, pw, test_dsn)

    if (datetime.datetime.now().time() < datetime.time(hour=18)):
        yesterday_str, today_str = GetDateStr(days_before=1)
    else:
        yesterday_str, today_str = GetDateStr() 

    print(yesterday_str, today_str)
    

