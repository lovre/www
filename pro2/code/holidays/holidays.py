import requests
import matplotlib.pyplot as plt

# https://podatki.gov.si/dataset/seznam-praznikov-in-dela-prostih-dni-v-republiki-sloveniji

json = requests.get("https://podatki.gov.si/api/3/action/datastore_search?resource_id=eb8b25ea-5c00-4817-a670-26e1023677c6&limit=10000").json()
data = json['result']['records']

years = list(range(2000, 2031))

holidays = {year: 0 for year in years}
freedays = {year: 0 for year in years}

for item in data:
  year = item['LETO']
  holidays[year] += 1
  if item['DELA_PROST_DAN'] == 'da' and item['DAN_V_TEDNU'] != 'sobota' and item['DAN_V_TEDNU'] != 'nedelja':
    freedays[year] += 1

fig = plt.figure()

plt.plot(years, [holidays[year] for year in years], '-o', label = "Prazniki")
plt.plot(years, [freedays[year] for year in years], '-s', label = "Dela prosti dnevi")

plt.ylim(0, 1.25 * max(holidays.values()))

plt.ylabel("Število dni")
plt.xlabel("Leto")
plt.legend()

fig.savefig("holidays.png", bbox_inches = 'tight')
