import http.client
import requests
import re

# establishes connection to FMF weekly schedule

conn = http.client.HTTPSConnection('urnik.fmf.uni-lj.si')

# creates request for schedule of 'Aplikativna matematika' (2nd year)

conn.request('GET', '/layer_one/44/?day=2025-02-25')

# retrieves schedule in format of HTML web page

page = conn.getresponse().read().decode()

# ** OR **

# establishes connection to FMF weekly schedule

res = requests.get('https://urnik.fmf.uni-lj.si/layer_one/44/?day=2025-02-25')

# retrieves schedule in format of HTML web page

page = res.text

# parses names of courses in schedule

courses = set()
for course in re.findall(r'<a href="/subject/[^>]+>[^<]+</a>', page):
  courses.add(re.split(r'[<>]', course)[2].strip())

# prints out names of courses in schedule

for i, course in enumerate(sorted(courses)):
  print("{:d}. {:s}".format(i + 1, course))
