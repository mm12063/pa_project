import csv

if __name__ == '__main__':
    file = open('data.csv')
    file_write = open('data2.csv', mode='w')
    csv_writer = csv.writer(file_write, delimiter=',')
    csv_reader = csv.reader(file, delimiter=',')
    index = 0
    for row in csv_reader:
        if row[0] != index:
            row[0] = index
            csv_writer.writerow(row)
        index += 1
    file.close()
    file_write.close()