from apikeys import *

import requests
import re

def address(location):
  """
  Find street address for given location using Google Maps API.
  """
  
  json = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + re.sub(r'\s', '+', location) + '&key=' + GOOGLE_KEY).json()
  
  street = None
  if len(json['results']) > 0:
    street = json['results'][0]['formatted_address']
    
  return street

LOCATIONS = [
  "Fakulteta za matematiko in fiziko",
  "Fakulteta za računalništvo in informatiko",
  "Univerza v Ljubljani",
  "Zavetišče Mačja hiša",
  "Cvetličarna"
]

for location in LOCATIONS:
  print(location)
  print(address(location))
  print()
