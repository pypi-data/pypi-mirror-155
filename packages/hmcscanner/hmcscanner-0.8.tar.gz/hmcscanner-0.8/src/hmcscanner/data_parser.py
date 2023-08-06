import csv
from io import StringIO

FILE = 'profile_example.txt'

data = []



def splitArray(s):
    if not ',' in s:
        return s

    f = StringIO(s)
    reader = csv.reader(f)
    for row in reader:
        return row




with open(FILE, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        d = { tuple(elem.split('=', 1)) for elem in row }
        d = { k:splitArray(v) for k, v in d }
        print(d)