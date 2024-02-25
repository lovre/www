from apikeys import *

import requests
import re

def similar(word):
  """
  Find similar word for given Slovenian word by scrapping Kontekst.io web page.
  If given word is capitalized, returned word is also capitalized.
  """
  if type(word) is re.Match:
    word = word.group()
    
  req = requests.get('https://kontekst.io/kontekst/' + re.sub(r'\s', '+', word.lower()))
  text = req.text
  
  res = re.search(r'<a ng-click="handleClick\(\$event\)" class="dictentry" id="[\sa-zčšž]+"\s*rel="nofollow">[\sa-zčšž]+</a>', text)
  sim = word if res is None else re.split('[<>]', res.group())[2].strip()
  
  return sim.capitalize() if word == word.capitalize() else sim

def translate(text, lang = 'en'):
  """
  Translate given Slovenian text into specified language using Google Translate API.
  """
  req = requests.get('https://translation.googleapis.com/language/translate/v2?q=' + re.sub(r'\s', '+', text) + '&source=sl&target=' + lang + '&key=' + GOOGLE_KEY)
  json = req.json()
  
  return json['data']['translations'][0]['translatedText']

# list of ten Slovenian proverbs

proverbs = ['Gliha vkup štriha.', 'Jezik z mošnjo raste.', 'Lakota je najboljši kuhar.', 'Za prepir sta potrebna dva.', 'En cvet še ne naredi pomladi.', 'Rožnik deževen viničar reven.', 'Visokim smrekam vihar vrhove lomi.', 'Odloženo delo obtožuje, zamujeno kaznuje.', 'Kdor gre na Dunaj, naj pusti trebuh zunaj.', 'Počasi se daleč pride, naglica koristi samo zajcem.']

# prints out synonyms and translations of Slovenian proverbs

for proverb in proverbs:
  print("{:>12s} | '{:s}'".format('Proverb', proverb))
  
  print("{:>12s} | '{:s}'".format('Similar', re.sub(r'[a-zčšžA-ZČŠŽ]+', similar, proverb)))
  
  print("{:>12s} | '{:s}'".format('EN', translate(proverb)))
  print("{:>12s} | '{:s}'".format('HR', translate(proverb, 'hr')))
  print("{:>12s} | '{:s}'".format('FR', translate(proverb, 'fr')))
  print("{:>12s} | '{:s}'\n".format('ZH', translate(proverb, 'zh-CN')))
