import requests

def actors(movies):
  cnts = {}
  for movie in movies:
    acts = movie['actors'].split(', ')
    for act1 in acts:
      for act2 in acts:
        if act1 < act2:
          pair = act1, act2
          if pair in cnts:
            cnts[pair] += 1
          else:
            cnts[pair] = 1
  return sorted(cnts.items(), key = lambda item: item[1])[-1]

movies = requests.get("https://lovro.fri.uni-lj.si/api/movies").json()

for genre in ["Action", "Drama", "Horror"]:
  (act1, act2), cnt = actors(movie for movie in movies if genre in movie['genres'])
  print(f"{genre}: {act1} & {act2} ({cnt} movies)")
