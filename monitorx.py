#!/usr/bin/python

from pymongo import MongoClient
from pprint import pprint
import subprocess
import string

#DBtest
client = MongoClient('mongodb://root:sg3043il@127.0.0.1:27017/')
db = client.subdomains

def diff(list1, list2):
    return (list(set(list1).symmetric_difference(set(list2))))

def addDomain():
    mycol = db["targets"]
    domain = str(input("Enter the domain to Monitor: "))
    print("Domain %s is added to the target list" % (domain))
    
    #Getting key value from db and incrementing it by 1 to add next domain in order

    cur = mycol.find().sort([('_id', -1)]).limit(1)
    for doc in cur:
        res = list(doc.keys())
    key_index = str(int(res[-1])+1)
    to_insert = {
            key_index: domain
            }
    db.targets.insert_one(to_insert)

def runOneScan():
    domain = str(input("Enter the domain to Scan: "))
    collection = db[domain]
    #reconx = subprocess.call(['./recon.sh', domain])


    with open(domain+'_dir/'+domain+'_final.txt', 'r') as program:
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

    collection.insert_one(data)

    if collection.find() == True:
        print("domain exists")#add compare logic here
        cursorNew = collection.find().sort([('_id', -1)]).limit(1)
        for doc in cursorNew:
            newRecord = list(doc.values())
            newRecord = newRecord[1:]
        cursorOld = collection.find().sort([('_id', -1)]).skip(1).limit(1)
        for docu in cursorOld:
            oldRecord = list(docu.values())
            oldRecord = oldRecord[1:]
        print(diff(oldRecord, newRecord))
    else:
        print("First occurence")
        myCursor = collection.find()
        for docuu in myCursor:
            firstRecord = list(docuu.values())
            firstRecord = firstRecord[1:]
            print(firstRecord)

def main():
    while True:
        print("----------------MONITOR-X---------------------\n")
        print("[1] - Add a Domain to monitoring list\n[2] - Run the scan against a particular domain\n[3] - Run scans against all domains\n[4] - Exit\nSelect your option: ")
        choice = int(input(">>> "))
        if choice==1:
            addDomain()
        elif choice==2:
            runOneScan()
        elif choice==3:
            runAllScan()
        elif choice==4:
            print("Bye")
            break
        else:
            print("Invalid Choice, please choose again\n")

if __name__ == "__main__":
    main()
