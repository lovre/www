from networks import Graph
import requests
import re

G = Graph('got_kills')

nodes = {}
for line in re.findall(r'<li>.+</li>', requests.get('https://listofdeaths.fandom.com/wiki/Game_of_Thrones').text):
  killing = re.sub(r'&#\d+;|\s+', ' ', re.sub(r'<.*?>|\(.*?\)', '', line)).split(' - ')
  
  if len(killing) == 2:
    killed, desc = killing
    
    killed = killed.replace('"', '')
    killer = re.search(r' by(\s[a-z]+){0,2}(\s[A-Z][a-z]+)+', desc)
    
    if killer != None:
      killer = re.search(r'[A-Z].*', killer.group()).group()

      if killed not in nodes:
        nodes[killed] = G.add_node(killed)
      if killer not in nodes:
        nodes[killer] = G.add_node(killer)
        
      G.add_edge(nodes[killer], nodes[killed])

Graph.write(G)

print(G)
