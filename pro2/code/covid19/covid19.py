import requests
import datetime

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

RED, GRAY = [0.73, 0.33, 0.33], [0.66] * 3

# COVID-19 source: https://www.ecdc.europa.eu/en/publications-data/data-daily-new-cases-covid-19-eueea-country

data = requests.get('https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/json').json()["records"]

# computes number of COVID-19 cases and deaths per day

cases, deaths = {}, {}
for entry in data:
  date = datetime.date(int(entry["year"]), int(entry["month"]), int(entry["day"]))
  
  if not date in cases:
    cases[date], deaths[date] = 0, 0

  if entry["cases"] != None:
    cases[date] += entry["cases"]
  if entry["deaths"] != None:
    deaths[date] += entry["deaths"]

dates = sorted(cases.keys())

# plots number of COVID-19 cases and deaths per day

fig = plt.figure(figsize = [12, 6])

plt.plot([date for date in dates if cases[date] > 0], [cases[date] for date in dates if cases[date] > 0], zorder = 0, \
  marker = 'o', markersize = 3, linewidth = 0, c = GRAY, markeredgecolor = GRAY, label = "Cases (per day)")
plt.plot([date for date in dates if deaths[date] > 0], [deaths[date] for date in dates if deaths[date] > 0], zorder = 1, \
  marker = '*', markersize = 5, linewidth = 0, c = RED, markeredgecolor = RED, label = "Deaths (per day)")

date = dates[len(dates) // 2]
plt.annotate("{:,d} cases".format(cases[date]), xy = (date, cases[date]), \
  xytext = (10, 50), textcoords = 'offset points', arrowprops = {'arrowstyle': '->'})
plt.annotate("{:,d} deaths".format(deaths[date]), xy = (date, deaths[date]), \
  xytext = (10, 50), textcoords = 'offset points', arrowprops = {'arrowstyle': '->'})

plt.yscale('log')
plt.xticks([dates[i * len(dates) // 7] for i in range(7)] + [dates[-1]])

plt.legend(loc = 'lower right', fontsize = 13)
plt.title("COVID-19 evolution", fontsize = 21, fontweight = 'bold')
plt.ylabel("Number cases & deaths", fontsize = 18)
plt.xlabel("Date", fontsize = 15)
plt.close()

fig.savefig('covid19-plot.pdf', bbox_inches = 'tight')

# computes number of COVID-19 cases and deaths by country

cases, deaths = {}, {}
for entry in data:
  country = entry["countryterritoryCode"]

  if not country in cases:
    cases[country], deaths[country] = 0, 0

  if entry["cases"] != None:
    cases[country] += entry["cases"]
  if entry["deaths"] != None:
    deaths[country] += entry["deaths"]

countries = sorted(cases.keys(), key = lambda country: -deaths[country])

# plots number of COVID-19 cases and deaths by country

fig = plt.figure(figsize = [15, 5])

plt.bar(countries, [cases[country] for country in countries], zorder = 0, \
  color = GRAY, edgecolor = 'black', label = "Cases (total)")
plt.bar(countries, [deaths[country] for country in countries], zorder = 1, \
  color = RED, edgecolor = 'black', label = "Deaths (total)")

plt.yscale('log')
plt.ylim(1, 10**9)

plt.legend(loc = 'upper right', fontsize = 13)
plt.title("COVID-19 by country", fontsize = 21, fontweight = 'bold')
plt.ylabel("Number cases & deaths", fontsize = 18)
plt.xlabel("Country", fontsize = 15)
plt.close()

fig.savefig('covid19-hist.pdf', bbox_inches = 'tight')

# collects detailed country information (population, location)

details = requests.get('https://lovro.fri.uni-lj.si/api/country').json()

countries = sorted(cases.keys(), key = lambda country: -cases[country] / details[country]["population"])

# maps number of COVID-19 cases and deaths by country

fig = plt.figure()

map = Basemap()
map.drawcountries()
map.drawcoastlines()
map.fillcontinents(color = [0.95] * 3)
#map.shadedrelief()
#map.bluemarble()

for i, country in enumerate(countries):
  plt.scatter([details[country]["longitude"]], [details[country]["latitude"]], zorder = 3 * i + 10, \
    marker = 'o', s = 500 * (cases[country] / details[country]["population"]), c = [GRAY + [0.75]], edgecolors = ['white'], \
    label = "Cases (total)" if country == "SVN" else None)
  plt.scatter([details[country]["longitude"]], [details[country]["latitude"]], zorder = 3 * i + 11, \
    marker = 'o', s = 10000 * (deaths[country] / details[country]["population"]), c = [RED], edgecolors = ['white'], \
    label = "Deaths (total)" if country == "SVN" else None)
  plt.text(details[country]["longitude"], details[country]["latitude"], details[country]["name"], zorder = 3 * i + 12, \
    fontsize = 4, horizontalalignment = 'center', verticalalignment = 'center')

plt.xlim(-22.5, 40)
plt.ylim(30, 67.5)

plt.legend(loc = 'lower left', fontsize = 8, frameon = False)
plt.title("COVID-19 geography", fontsize = 13, fontweight = 'bold')
plt.close()

fig.savefig('covid19-map.pdf', bbox_inches = 'tight')
