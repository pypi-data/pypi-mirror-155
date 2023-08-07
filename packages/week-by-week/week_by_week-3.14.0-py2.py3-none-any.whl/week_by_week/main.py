from pandas import Timestamp
import pandas as pd

# df = pd.read_csv('./raw_events.csv')

class WeekRange:
    ''''
    This Library accept pandas dataframe, date_column and optional end date
    If end date is not provide, current today will be use internally by the library
    params:
        df -> pandas dataframe
        date_column -> a column in the dataframe which is of date(Timestamp) object
        tested with virieties of date format, it use pd.to_datetime under the hood
        end_date = last date to which week will be calculated
        WK_start='Mon' default is 'Mon', it can be change to 'Sun' This signify 
        the first day of the week


    Required parameter are:
    1. df -- pandas dataframe
    2. timestamp -- date columnin your df
    3. WK_start change between 'Mon' to 'Sun'
    Optional parameter:
        1. end_date

    call ```getAllweeks()`` method to retrieve all weeks       
    ```weeks = get_weeks.getAllweeks()```


    And to retrieve data splitted into week range,
    invoke ```getWeekData()``` 

    `print(get_weeks.getWeekData())`

    '''
    def __init__(self, df, date_column, end_date=None,WK_start='Mon') -> None:
        self.df = df
        self.WK_start = WK_start
        self.df_columns = self.df.columns[:]
        try:
            if end_date != None:
                self.current_date = pd.Timestamp(pd.to_datetime(end_date))
            else:
                self.current_date = self.getCurrentDay()
            
            first_date_occurrence = self.getfirst_date(self.df, date_column)
            self.week_offset = self.get_week_offset()
            

            if self.week_offset != -1:
                self.first_last_weekend = self.get_date_weekday(first_date_occurrence, self.week_offset)[1]
            else:
                raise Exception("Invalid Begin of Week") 
                
        except AttributeError:
            print('Invalid Begin ofWeek')


    def get_week_offset(self):
        if self.WK_start.lower() == 'sun':
            return 0
        elif self.WK_start.lower() == 'mon':
            return 1
        else:
            return -1

    def getCurrentDay(self):
        return pd.Timestamp(pd.to_datetime("today").date())

    def getfirst_date(self, df, date_column):
        df = df.sort_values(by=[date_column], ascending=True)
        df[date_column] = df[date_column]
        df = pd.to_datetime(df[date_column])
        last_day = df.iloc[0:1]
        return last_day.values[0]

    def get_date_weekday(self, datevalue :Timestamp, week_offset: int) -> list:
        day_in_Week= pd.to_datetime(datevalue)
        date_pos_in_weekday = day_in_Week.isoweekday()
        week_start = day_in_Week - pd.Timedelta(days=date_pos_in_weekday - week_offset)
        week_end = week_start + pd.Timedelta(days=6)
        
        return (week_start, week_end)

    def getAllweeks(self) -> list:
        '''Get beginning and end of each week since the first_occurrence date
        item1 = [week_start, week_end]
        week_interval = ([week_start, week_end], [week_start, week_end])
        '''

        last_week_end = self.first_last_weekend - pd.Timedelta(days=7) #Fix weekend before the first data point
        box_week = []

        while last_week_end < self.current_date:
            next_week_end = last_week_end + pd.Timedelta(days=7)
            box_week.append([last_week_end + pd.Timedelta(days=1), next_week_end])
            last_week_end = next_week_end
        return box_week



    def getWeekData(self):
        all_week_range = self.getAllweeks()
        dataDict = dict()
        for week_range  in all_week_range:
            week_data = list()
            for id, event, timestamp in zip(self.df[self.df_columns[0]], self.df[self.df_columns[1]], self.df[self.df_columns[2]]):
                if pd.Timestamp(timestamp) >= week_range[0] and pd.Timestamp(timestamp) <= week_range[1]:
                    week_data.append((id, event, timestamp))
            if len(week_data) == 0:continue
            else:
                dataDict[week_range[0]] = week_data
        return dataDict


    def retunpandasDF(self):
        '''
        Return each week dataframe when the method is invoke
        
        '''
        data = self.getWeekData()
        df = pd.DataFrame()
        key_list = list(data.keys())
        counter = 0 
        num_week = len(key_list)
        while counter < num_week:
            # print(key_list[counter])
            values = data.get(key_list[counter])
            df[[self.df_columns[0], self.df_columns[1], self.df_columns[2]]] = \
                values
            
            yield df
            df = df[0:0] # Clear previous week data
            counter += 1
        



    # TODO 
    # 1. 


# get_weeks = WeekRange(df, 'timestamp','2022/06/01', WK_start='sun')
# # weeks = get_weeks.getAllweeks()



# # for week in get_weeks.retunpandasDF():
# #     print(week)