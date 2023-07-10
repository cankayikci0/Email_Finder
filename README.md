# Email_Finder

# Email Finder - Responsible Web Scraping for Research and Outreach

This project provides a web scraping tool designed to extract email addresses from specified CSV file URLs. It aims to facilitate legitimate research and outreach activities, allowing users to gather contact information for networking.

## Features

- Parses CSV file to identify and extract urls.
- Sends requests to these urls and update the table with the status code.
- If the status code is 200, it gets the raw html code and extracts the emails with regex
- The regex can prevent basic level email obfuscating.

