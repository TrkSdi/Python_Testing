import json

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions
     
     
competitions = loadCompetitions()
clubs = loadClubs()

    
def add(a, b):
    return a + b

print(add([1, 3], [2]))