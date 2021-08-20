from time import *
import requests
import re

def similar(word):
  """
  Find similar word for given Slovenian word by scrapping Kontekst.io web page.
  If given word is capitalized, returned word is also capitalized.
  """
  word = word.group()
  req = requests.get('https://kontekst.io/kontekst/' + word.lower())
  res = re.search(r'<a ng-click="handleClick\(\$event\)" class="dictentry" id="[a-zčšž]+"\s*rel="nofollow">[\sa-zčšž]+</a>', req.text)
  sim = word if res is None else re.sub(r'<.*?>', '', re.sub(r'\s', '', res.group()))
  return sim.capitalize() if word == word.capitalize() else sim

def translate(text, lang = 'en'):
  """
  Translate given Slovenian text into specified language using Google Translate API.
  """
  return requests.get('https://translation.googleapis.com/language/translate/v2?q=' + re.sub(r'\s', '+', text) + '&source=sl&target=' + lang + '&key=' + GOOGLE_KEY).json()['data']['translations'][0]['translatedText']

start = time()

# list of ten Slovenian proverbs

proverbs = ['Vse je šlo za med.', 'Jezik z mošnjo raste.', 'Lakota je najboljši kuhar.', 'Za prepir sta potrebna dva.', 'En cvet še ne naredi pomladi.', 'Rožnik deževen viničar reven.', 'Visokim smrekam vihar vrhove lomi.', 'Odloženo delo obtožuje, zamujeno kaznuje.', 'Kdor gre na Dunaj, naj pusti trebuh zunaj.', 'Počasi se daleč pride, naglica koristi samo zajcem.']

# prints out synonyms and translations of Slovenian proverbs

for proverb in proverbs:
  print("{:>12s} | '{:s}'".format('Proverb', proverb))
  print("{:>12s} | '{:s}'".format('Synonym', re.sub(r'[a-zčšžA-ZČŠŽ]+', similar, proverb)))
  print("{:>12s} | '{:s}'".format('HR', translate(proverb, 'hr')))
  print("{:>12s} | '{:s}'".format('EN', translate(proverb)))
  print("{:>12s} | '{:s}'".format('DE', translate(proverb, 'de')))
  print("{:>12s} | '{:s}'".format('FR', translate(proverb, 'fr')))
  print("{:>12s} | '{:s}'\n".format('ZH', translate(proverb, 'zh-CN')))

print("{:>12s} | {:.1f} sec\n".format('Time', time() - start))
