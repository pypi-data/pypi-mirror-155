# This package "week by Week" 
is attempt to have Python library that 
1. Generate week range from pandas dataframe from the first
   data point date to the current or a given date
2. Group pandas row into weekly base on the date/timestamp column

# Usage after installation
```from week_by_week import WeekRange```

Instantiate the class
```get_weeks = WeekRange(df, 'timestamp','2022/06/01', WK_start='sun')```

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



