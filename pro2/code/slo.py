from google import *
from time import *
import requests
import random
import re

def search(city):
  """
  Get number of web pages about given Slovenian city using Google Search API.
  """
  res = requests.get('https://www.googleapis.com/customsearch/v1?q=' + re.sub(r'\s', '+', city) + ',+Slovenia&cx=' + GOOGLE_ID + '&key=' + GOOGLE_KEY).json()
  return int(res['searchInformation']['totalResults']) if 'searchInformation' in res else 0

def location(city):
  """
  Get latitue and longitude of given Slovenian city using Google Maps API.
  """
  loc = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + re.sub(r'\s', '+', city) + ',+Slovenia&key=' + GOOGLE_KEY).json()['results'][0]['geometry']['location']
  return (loc['lat'], loc['lng'])

start = time()

# gets Slovenian cities with ZIP codes using Dejan Lavbič's API

cities = requests.get('https://api.lavbic.net/kraji').json()

random.shuffle(cities)

# prints out names, ZIP codes, locations and search results of Slovenian cities

for i, city in enumerate(cities):
  loc = location(city['kraj'])
  print("{:>12s} | {:d}".format('ZIP', city['postnaStevilka']))
  print("{:>12s} | '{:s}, Slovenija'".format('City', city['kraj']))
  print("{:>12s} | ({:.3f}, {:.3f})".format('Location', loc[0], loc[1]))
  print("{:>12s} | {:,d} pages\n".format('Google', search(city['kraj'])))
  if i == 14:
    break

print("{:>12s} | {:.1f} sec\n".format('Time', time() - start))
