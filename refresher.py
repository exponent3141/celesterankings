#1A88F3X2lOQJry-Da2NpnAr-w5WDrkjDtg7Wt0kLCiz8
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pickle
from math import ceil
from random import randint
spreadsheet_id = '1A88F3X2lOQJry-Da2NpnAr-w5WDrkjDtg7Wt0kLCiz8'
# For example:
# spreadsheet_id = "8VaaiCuZ2q09IVndzU54s1RtxQreAxgFNaUPf9su5hK0"

credentials = service_account.Credentials.from_service_account_file("key.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
service = build("sheets", "v4", credentials=credentials)

request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="Clears")
sheet_props = request.execute()


thmb = service.spreadsheets().get(spreadsheetId=spreadsheet_id,fields="sheets/data/rowData/values/hyperlink").execute()

vs = sheet_props['values']
players = vs[0][3:]
maps = {}
playerscores = {i:[] for i in players} 



for i in vs[1:-1]:
    if len(i)>3:
        scores = i[3:]
        maps[i[0]] = []
        for j in range(len(scores)):
            if scores[j]!='':
                maps[i[0]].append(players[j])
                playerscores[players[j]].append(i[0])

star = 7
stars = {}
amount = {1:0,2:0,3:0,4:0, 5:0, 6:0, 7:0, 8:0}
div = {2:2, 1:2}
map_names = []
for i in vs[1:-1]:
    if i==[]:
        posss +=1
    elif 'Ranked'  in i[0] or 'Subtiered' in i[0]:
        star-=1
        star = ceil(star)
        posss = 1
        if 'Ranked' in i[0]:
            divided = False
        else:
            divided = True
        
    else:
        map_names.append(i[0])
        stars[i[0]]= [star]
        if not divided:
            stars[i[0]].append(posss)
            posss+=1
        else:
            stars[i[0]].append(posss)
        amount[star]+=1
        
for i in amount.keys():
    if i not in div:
        div[i] = amount[i]

def getElo(star, nDiv, pos):
    '''star is the star ranking of the map (duh)
    nDiv is the number of divisions of this star ranking
    pos is the position of the map within the divisions, 1<=pos<=nDiv, 1 is highest rated (hardest). 
    ....did i actually just use a docstring as intended
    f'''
    ratings = {1:(100,200), 2:(300,400), 3:(500,750), 4:(800,1000), 5:(0,0), 6:(0,0)}
    
    try:
        posFix = nDiv-pos
        rRange = ratings[star][1] - ratings[star][0]
        return ratings[star][0] + ((rRange/(nDiv-1))*(posFix) if nDiv != 1 else rRange//2)
    except KeyError:
        raise KeyError(f'You need to add data for {star} star to the ratings dict! (you idiot)')


eloo = {}
for i in stars.keys():
    b_s, b_p = stars[i]
    eloo[i] = getElo(b_s, div[b_s], b_p)


playerelo = {i:[0,0] for i in players}
playereloRat = {i:[0,0] for i in players}

player_names = list(playerelo.keys())
nametoid = {player_names[i]:i for i in range(len(player_names))}
maptoid = {map_names[i]:i for i in range(len(map_names))}
badges = {i:{} for i in player_names}
playerstarcount = {i:{1:0, 2:0, 3:0,4:0} for i in player_names}


for mapy, mapp in maps.items():
    for pl in mapp:
        playerstarcount[pl][stars[mapy][0]]+=1


for i in playerscores.items():
    cancercoefficient = 1
   # pissmap = sorted(i[1], key=lambda a: eloo[a])
    for dmap in i[1]:
        playerelo[i[0]][0]+=eloo[dmap]*cancercoefficient
        playerelo[i[0]][1]+=1
        cancercoefficient*=0.90

    playereloRat[i[0]][0] = randint(1,999)
    playereloRat[i[0]][1] = randint(1,50)

print(playerelo['snoot'])
for i in player_names:
    subject = playerstarcount[i]
    if subject[1]>0:
        badges[i][1]=1
        if subject[1]==amount[1]:
            badges[i][1]=2
    else:
        badges[i][1]=0

    if subject[2]>0:
        badges[i][2]=1
        if subject[2]==amount[2]:
            badges[i][2]=2
    else:
        badges[i][2]=0

    if subject[3]>0:
        badges[i][3]=1
        if subject[3]==amount[3]:
            badges[i][3]=2
    else:
        badges[i][3]=0

  

pll = sorted(list(playerelo.items()), key= lambda x: x[1][0], reverse=True)

rank = 1
prev_elo = None
ranked_players = []
for i, (name, elo) in enumerate(pll):
    if elo[0] != prev_elo:
        rank = i + 1
    ranked_players.append([name, elo[0], rank, elo[1]])
    playerelo[name].append(rank)
    prev_elo = elo[0]

for i in range(len(ranked_players)):
    ranked_players[i].append(nametoid[ranked_players[i][0]])

#bro idk what this code is doing 😋
pllLeaEdition = sorted(list(playereloRat.items()), key= lambda x: x[1][0], reverse=True)
leaified_players = []
ratRank = 1
prelo_rat = None
for i, (name, elo) in enumerate(pllLeaEdition):
    if elo[0] != prelo_rat:
        ratRank = i + 1
    leaified_players.append([name, elo[0], ratRank, elo[1]])
    playereloRat[name].append(rank)
    prelo_rat = elo[0]

for i in range(len(leaified_players)):
    leaified_players[i].append(nametoid[leaified_players[i][0]])



#name, elo, rank, number of maps completed, id
thf = []
for i in range(100):
    try:
        thf.append(thmb['sheets'][1]['data'][0]['rowData'][i]['values'][2]['hyperlink'])
    except Exception as e:
        print(e)
thr = {}
for i in range(len(map_names)):
    try:
        thr[map_names[i]]=thf[i]
    except:
        print(f"throw at {i}")
for j, i in enumerate(map_names):
    stars[i].append(eloo[i])
    try:
        stars[i].append(len(maps[i]))
    except:
        stars[i].append(0)
    stars[i][1] = j+1


for i in ranked_players:
    print(f"#{i[2]}: {i[0]} elo: {i[1]}")
print(stars)
with open('players.pkl', 'wb') as f:
          pickle.dump(ranked_players, f)
with open('playersRandom.pkl', 'wb') as f:
          pickle.dump(leaified_players, f)
with open('maps.pkl', 'wb') as f:
          pickle.dump(stars, f)
with open('playermaps.pkl', 'wb') as f:
    pickle.dump(playerscores, f)
with open('playerstats.pkl', 'wb') as f:
    pickle.dump(playerelo, f)
with open('playerstatsRandom.pkl', 'wb') as f:
    pickle.dump(playereloRat, f)
with open('mapid.pkl', 'wb') as f:
    pickle.dump(maptoid, f)
with open('Lmaps.pkl', 'wb') as f:
        pickle.dump(maps, f)

with open('badges.pkl', 'wb') as f:
    pickle.dump(badges,f)



# Output:
# My New Google Sheets Spreadsheet
