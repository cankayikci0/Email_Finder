import os
import sqlite3
import datetime
import csv


def createDatabase(databaseName):
	if os.path.exists(databaseName):
		os.remove(databaseName)
		print("Existing database removed.")

	conn = sqlite3.connect(databaseName)
	cur = conn.cursor()
	
	cur.execute("""
		CREATE TABLE IF NOT EXISTS my_table (
		id INTEGER,
		url TEXT,
		responsecode INTEGER NULL,
		mails TEXT NULL,
		lastChecked timestamp NULL
		);
		""")

	return cur

def insertTable(id, url, cur):
	
	sqlite_insert_with_param = """INSERT INTO 'my_table'
						  ('id', 'url') 
						  VALUES (?, ?);"""

	data_tuple = (id, url)
	cur.execute(sqlite_insert_with_param, data_tuple)
	

	return 0


def readFromFile():
	try:
		with open('contacts_report.csv', 'r', encoding="utf-8", errors = "ignore") as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',', quotechar=',',quoting=csv.QUOTE_MINIMAL)
			
			cur = createDatabase("testttt.db") #  name of the database    <---
			
			a = 0
			url_set = set()
			for row in csv_reader:
				url_set.add(row[0])

				a += 1
				if row[1]:
					url_set.add(row[1])		   #   arrangement while reading from file <---
				
		id = 1
		for url in url_set:
				#print(url)
			insertTable(id, url, cur)	
			id += 1               
				
			#print(len(url_set))

		#cur.execute("SELECT * FROM my_table")  #   print whether everything is OK.
		#result = cur.fetchall()
		#print(result)
		
		return cur

	except FileNotFoundError as e:
		print("File not found.")
		return False

def main():	
	readFromFile()
	return 0





if __name__ == '__main__':
	main()


