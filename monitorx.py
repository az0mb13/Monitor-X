#!/usr/bin/python

from pymongo import MongoClient
from pprint import pprint
import subprocess
import string

#DBtest
client = MongoClient('mongodb://root:sg3043il@127.0.0.1:27017/')

target = str(input("Enter the domain to Monitor: "))
print(target)
#reconx = subprocess.call('./recon.sh')

#appending line numbers to convert to dict json
with open('tedtest', 'r') as program:
    data = program.readlines()

with open('outfile', 'w') as program:
    for (number, line) in enumerate(data):
        program.write('%d %s' % (number + 1, line))

#converting file to json to add to db
data = {}
with open("outfile") as f:
    for line in f:
        (key, val) = line.split()
        data[(key)] = val
        
db = client.subdomains
collection = db.target

collection.insert_one(data)
