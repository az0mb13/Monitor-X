#!/usr/bin/python

import os
import slack
from pymongo import MongoClient
import subprocess
import string
import requests

#SlackTest
#sClient = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])


#DBtest
client = MongoClient('mongodb://root:sg3043il@127.0.0.1:27017/')
db = client.subdomains

def converttostr(input_seq, seperator):
   # Join all the strings in list
   final_str = seperator.join(input_seq)
   return final_str

def diff(list1, list2):
    return (list(set(list1).symmetric_difference(set(list2))))

def showDomains():
	mycol = db["targets"]
	domains = mycol.find()
	for doc in domains:
		print(doc)

def addDomain():
    mycol = db["targets"]
    domain = str(input("Enter the domain to Monitor: "))
    print("Domain %s is added to the target list" % (domain))
    key_index = "1"
    to_insert = {
            key_index: domain
            }
    #Getting key value from db and incrementing it by 1 to add next domain in order
    if mycol.find().count() > 0:
    	cur = mycol.find().sort([('_id', -1)]).limit(1)
    	for doc in cur:
    	    res = list(doc.keys())
    	key_index = str(int(res[-1])+1)
    	to_insert = {
    	        key_index: domain
    	        }
    	db.targets.insert_one(to_insert)
    else:
    	db.targets.insert_one(to_insert)
    #TESTING SLACK
    #command = "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\" added to targets\" +domain+ \"\"}' https://hooks.slack.com/services/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"
    data = {"text": domain+" added to targets"}
    response = requests.post('https://hooks.slack.com/services/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', json=data)
    print(response.status_code)
    

def compare(collection):
	print("Collection count is :", collection.count())
	if collection.count() > 1:
	    #print("domain exists")#add compare logic here
	    cursorNew = collection.find().sort([('_id', -1)]).limit(1)
	    for doc in cursorNew:
	        newRecord = list(doc.values())
	        newRecord = newRecord[1:]
	    cursorOld = collection.find().sort([('_id', -1)]).skip(1).limit(1)
	    for docu in cursorOld:
	        oldRecord = list(docu.values())
	        oldRecord = oldRecord[1:]
	        difference = str(diff(oldRecord, newRecord))
	        difference = difference[2:-2]
	        data = {"text": "New subdomain added/removed: "+difference}#improve this feature to detect add/remove
	        response = requests.post('https://hooks.slack.com/services/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', json=data)
	        print(response.status_code)
	if collection.find().count() == 1:
	    myCursor = collection.find()
	    for docuu in myCursor:
	        firstRecord = list(docuu.values())
	        firstRecord = firstRecord[1:]
	        separator = '\n'
	        firstRecord = converttostr(firstRecord, separator)
	        data = {"text": "First scan done:\n"+firstRecord}
	        response = requests.post('https://hooks.slack.com/services/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', json=data)
	        print(response.status_code)

def runOneScan():
    domain = str(input("Enter the domain to Scan: "))
    collection = db[domain]
    #subprocess.call(['./recon.sh', domain])


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
    compare(collection)

def runAllScan():
    collection = db["targets"]
    if collection.find() == False:
        print("No domain in the database. Add a domain and run the tool again")
    else:
        targetCursor = collection.find()
        for d in targetCursor:
            targetList = list(d.values())
            targetList = str(targetList[1:])
            targetList = targetList[2:-2]
            #subprocess.call(['./recon.sh', targetList])
            coll = db[targetList]
            with open(targetList+'_dir/'+targetList+'_final.txt', 'r') as program:
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

            coll.insert_one(data)
            compare(coll)

def main():
    while True:
    	subprocess.call('clear',shell=True)
    	print("""
    		  ▄▄▄▄███▄▄▄▄    ▄██████▄  ███▄▄▄▄    ▄█      ███      ▄██████▄     ▄████████ 		▀████    ▐████▀ 
    		▄██▀▀▀███▀▀▀██▄ ███    ███ ███▀▀▀██▄ ███  ▀█████████▄ ███    ███   ███    ███ 		  ███▌   ████▀  
    		███   ███   ███ ███    ███ ███   ███ ███▌    ▀███▀▀██ ███    ███   ███    ███ 		   ███  ▐███    
    		███   ███   ███ ███    ███ ███   ███ ███▌     ███   ▀ ███    ███  ▄███▄▄▄▄██▀ 		   ▀███▄███▀    
    		███   ███   ███ ███    ███ ███   ███ ███▌     ███     ███    ███ ▀▀███▀▀▀▀▀   		   ████▀██▄     
    		███   ███   ███ ███    ███ ███   ███ ███      ███     ███    ███ ▀███████████ 		  ▐███  ▀███    
    		███   ███   ███ ███    ███ ███   ███ ███      ███     ███    ███   ███    ███ 		 ▄███     ███▄  
    		 ▀█   ███   █▀   ▀██████▀   ▀█   █▀  █▀      ▄████▀    ▀██████▀    ███    ███ 		████       ███▄ 
    		                                                                   ███    ███                 
    		""")
    	print("----------------Subdomain Monitoring and SlackBot---------------------\n")
    	print("[1] - Add a Domain to monitoring list\n[2] - Show all domains\n[3] - Run the scan against a particular domain\n[4] - Run scans against all domains\n[5] - Exit\nSelect your option: ")
    	choice = int(input(">>> "))
    	if choice==1:
    	    addDomain()
    	elif choice==2:
    		showDomains()
    	elif choice==3:
    	    runOneScan()
    	elif choice==4:
    	    runAllScan()
    	elif choice==5:
    	    print("Bye")
    	    break
    	else:
    	    print("Invalid Choice, please choose again\n")

if __name__ == "__main__":
    main()
