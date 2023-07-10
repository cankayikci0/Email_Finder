import sqlite3
import db_init as db
import requests
import random
from requests_html import HTMLSession
import re
import datetime



def sendRequest():
	cur = db.readFromFile()


	#finding the range of the numbers
	cur.execute("SELECT id FROM my_table")
	ids = cur.fetchall()
	last_id = ids[-1]
	starting_id = 1
	ending_id = last_id[0]
	numbers = list(range(starting_id, ending_id + 1))
	random.shuffle(numbers)

	lastCheck = datetime.datetime.today().strftime("%x") #datetime.datetime.now() can also be used
	#month/day/year


	while numbers:
		session = HTMLSession()
		#random id number in a certain range
		random_id = numbers.pop()
		#print(random_id)
		selectArgument = "SELECT url FROM my_table WHERE id = ?;"
		cur.execute(selectArgument, [random_id])
		url = cur.fetchall()

		

		result = url[0][0]
		#request
		r = session.get(result)
		#response = requests.get(result, headers=headers)

		updateArgument = "UPDATE my_table SET responsecode = ?, lastChecked = ? WHERE id = ?;"
		cur.execute(updateArgument, [r.status_code, lastCheck,random_id])

		# I've developed this regex. It is still open to be improved. 
		# Catches emails like
		# example@gmail.com		example (at) gmail(dot).com
		# example(at)gmail.com	example (at) gmail.com
		# example(at)gmail [dot} com 
		# And it goes on...
		
		EMAIL_REGEX = r"""[a-zA-Z]+( ?(@|[({\[]\s*at\s*[)}\]]|[({\[]\s*@\s*[)}\]]) ?)[a-zA-Z-]+ ?(\.|[({\[]\s*dot\s*[)}\]]|[({\[]\s*\.\s*[)}\]])(?!jpe?g$)(?!png$) ?[a-zA-Z0-9-.]+[a-zA-Z0-9-.]+"""
		
		#r"[A-Z0-9._%+-]+(\s*@\s*|\s*\[|\{\(\s*(?:at|@)\s*\)\}\]\s*)([A-Z0-9.-]+(\.|\s*\[|\{\(\s*(?:dot|\.)\s*\)\}\]\s*)[a-z]+)+"
		
		found_emails = set() # created a set in order to save unique mails
		for re_match in re.finditer(EMAIL_REGEX, r.html.raw_html.decode('utf-8', errors='ignore'), re.IGNORECASE):
			result = str(re_match)

			# Saving in a proper format if there is any email obfuscation

			if re_match.group(1) != "@":
				replacement = r" ?[({\[]\s*at\s*[)}\]] ?| ?[({\[]\s*@\s*[)}\]] ?"
				result = re.sub(replacement, "@", result)

			if re_match.group(2) != ".":
				replacement = r" ?[({\[]\s*dot\s*[)}\]] ?| ?[({\[]\s*\.\s*[)}\]] ?"
				result = re.sub(replacement, ".", result)

			found_emails.add(result.split("'")[1])

		if found_emails:
			print(found_emails)
			emailArgument = "UPDATE my_table SET mails = ? WHERE id = ?"
			cur.execute(emailArgument, [", ".join(found_emails), random_id])
		

	# Check whether everything is OK
	cur.execute("SELECT * from my_table;")
	result = cur.fetchall()
	print(result)
	return 0




def main():	
	sendRequest()
	return 0



if __name__ == '__main__':
	main()



