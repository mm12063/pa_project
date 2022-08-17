import csv
import os

SEARCH_COLUMN = 'text'
SEARCH_TERMS = ['something', 'wicked', 'this', 'way', 'comes'] 
# This'd be an AND filter. That is, the code will filter out columns that contains ALL of the terms in the SEARCH_TERMS list

def create_dest_filename(filename : str) -> str:
    splitext = os.path.splitext(os.path.basename(filename))
    return os.path.join(os.path.dirname(filename), splitext[0] + '_filtered' + splitext[1])

def search_term_there(text):
    there = True
    for term in SEARCH_TERMS:
        there = there and (term in text)
    return there

def filter(filename : str) -> None:
    file = open(filename, 'r')
    csv_reader = csv.reader(file)
    destfile = open(create_dest_filename(filename), 'w')
    csv_writer = csv.writer(destfile)
    columns = next(csv_reader)
    csv_writer.writerow(columns)
    column_index = columns.index(SEARCH_COLUMN)
    for row in csv_reader:
        if search_term_there(row[column_index]):
            csv_writer.writerow(row)
    file.close()
    destfile.close()


if __name__ == '__main__':
    filename = 'something.csv'
    filter(filename)