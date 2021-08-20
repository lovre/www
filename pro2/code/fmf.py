import http.client
import requests
import re

# establishes connection to FMF weekly schedule

conn = http.client.HTTPSConnection('urnik.fmf.uni-lj.si')

# creates request for schedule of 'Praktična matematika' (2nd year)

conn.request('GET', '/letnik/44/')

# retrieves schedule in format of HTML web page

page = conn.getresponse().read().decode()

# ** OR **

# establishes connection to FMF weekly schedule

req = requests.get('https://urnik.fmf.uni-lj.si/letnik/44/')

# retrieves schedule in format of HTML web page

page = req.text

# parses names of courses in schedule

courses = set()
for course in re.findall(r'<a href="/predmet/\d+/">[^<]+</a>', page):
  courses.add(re.sub(r'^\s+', '', re.split('\n', course)[1]))

# prints out names of courses in schedule

for i, course in enumerate(sorted(courses)):
  print("{:2d}. {:s}".format(i + 1, course))
