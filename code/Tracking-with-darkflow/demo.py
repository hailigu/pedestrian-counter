'''Test GetCsvColumn'''

import csv
from GetCsvColumn import CsvFile,EXCLUDE

csvfilename = 'test.avi.csv'
csvfile = CsvFile(csvfilename)

with open(csvfilename,'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    column = [row['track_id'] for row in reader]
    blist = set(column)
print 'count:'
print ("count: %d" %(len(blist)))
