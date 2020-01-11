#!/usr/bin/python

from pymongo import MongoClient
from pprint import pprint
import subprocess
import string

#DBtest
client = MongoClient('mongodb://root:sg3043il@127.0.0.1:27017/')
db = client.subdomains

def addDomain():
    domain = str(input("Enter the domain to Monitor: "))
    #print(domain)
    db.targets.insert(domain)


def runScan():
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
        
    collection = db.target
    collection.insert_one(data)


def main():
    while True:
        print("MONITOR-X\n")
        print("[1] - Add a Domain to monitoring list\n[2] - Run the scan against a particular domain\n[3] - Run scans against all domains\n[4] - Exit\nSelect your option: ")
        choice = int(input(">>> "))
        if choice==1:
            addDomain()
        elif choice==2:
            runOneScan()
        elif choice==3:
            runAllScan()
        elif choice==4:
            break()
        else:
            print("Invalid Choice, please choose again\n")

