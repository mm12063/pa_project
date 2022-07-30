import datetime

date_range_st = datetime.date(2015, 1, 1)
date_range_end = datetime.date(2019, 12, 31)


def get_date_parts(date):
    temp_day = int(datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%d'))
    temp_month = int(datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%m'))
    temp_year = int(datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%Y'))
    return temp_day, temp_month, temp_year