import re
import csv
import os

# Code for transforming various kinds of input date times to target dd/mm/yyyy format
DROP_COLUMN = False
COLUMN_NAME = 'content'

def get_dest_name(filepath: str) -> str:
    basename_split = os.path.splitext(os.path.basename(filepath))
    dirname = os.path.dirname(filepath)
    dirname = os.path.join(dirname, 'fixed')
    os.makedirs(dirname, exist_ok = True)
    return os.path.join(dirname,  basename_split[0] + '_fixed' + basename_split[1])

# yyyy-mm-dd
def transform1(date : str) -> str:
    pattern = re.compile(r'\d\d\d\d-\d\d-\d\d')
    mo = pattern.search(date)
    actual_date = mo.group()
    return actual_date[-2:] + '/' + actual_date[5:7] + '/' + actual_date[:4]

# mm/dd/yyyy
def transform2(date : str) -> str:
    pattern = re.compile(r'\d\d/\d\d/\d\d\d\d')
    mo = pattern.search(date)
    actual_date = mo.group()
    return actual_date[3:5] + '/' + actual_date[:2] + '/' + actual_date[-4:]

def transform(date):
    return transform1(date)
    # return transform2(date)
    
def fix_dates(filename: str) -> None:
    file = open(filename, 'r')
    # file = open(filename, 'r')
    csv_reader = csv.reader(file, delimiter = ',')
    columns = next(csv_reader)
    destname = get_dest_name(filename)
    destfile = open(destname, 'w')
    csv_writer = csv.writer(destfile)
    date_index = columns.index('date')
    if DROP_COLUMN:
        drop_index = columns.index(COLUMN_NAME)
        columns = columns[:drop_index] + columns[drop_index + 1:]
    csv_writer.writerow(columns)
    for row in csv_reader:
        row[date_index] = transform(row[date_index])
        if DROP_COLUMN:
            row = row[:drop_index] + row[drop_index + 1:]
        csv_writer.writerow(row)
    file.close()
    destfile.close()

def test():
    given_date = '2018-11-26 06:26:04-04:00'
    print("given_date: " + given_date)
    print(transform(given_date))

if __name__ == '__main__':
    file = 'all_data/ALB/($ALB).csv'
    # test()
    fix_dates(file)
    