#1A88F3X2lOQJry-Da2NpnAr-w5WDrkjDtg7Wt0kLCiz8
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pickle
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

star = 4
stars = {}
amount = {1:0,2:0,3:0}
for i in vs[1:-1]:
    if 'Ranked'  in i[0] or 'Alphabetical' in i[0]:
        star-=1
    else:
        stars[i[0]]= [star]
        amount[star]+=1

        
def starfunction(star, rank):
    #amount = {1:23, 2:11, 3:7}

    rangeStart = {1: 1, 2: 2, 3: 4} #starting point of each range
    rangeLen = {1: 100, 2: 100, 3: 100} #untested i wouldn't change this if i were you

    amountFix = [0, amount[1], amount[1]+amount[2]] #, ...

    if star == 1:
        return rangeStart[1]*rangeLen[1]

    rRank = ((len(maps)) - (rank))-amountFix[star-1] #???
    return (rangeStart[star] + (1/(amount[star]-1))*rRank)*rangeLen[star]





for j,i in enumerate(stars.keys()):
    stars[i].append(j+1)
    stars[i].append(starfunction(stars[i][0], stars[i][1]))
    stars[i].append(len(maps[i]))


playerelo = {i:[0] for i in players}
player_names = list(playerelo.keys())
map_names = list(maps.keys())
nametoid = {player_names[i]:i for i in range(len(player_names))}

maptoid = {map_names[i]:i for i in range(len(map_names))}

badges = {i:{} for i in player_names}
playerstarcount = {i:{1:0, 2:0, 3:0} for i in player_names}


for mapy, mapp in maps.items():
    for pl in mapp:
        playerelo[pl][0]+=stars[mapy][-2]
        playerstarcount[pl][stars[mapy][0]]+=1

for i in playerscores.items():
    playerelo[i[0]].append(len(i[1]))

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
        print(f"trhow at {i}")
with open('players.pkl', 'wb') as f:
          pickle.dump(ranked_players, f)
with open('maps.pkl', 'wb') as f:
          pickle.dump(stars, f)
with open('playermaps.pkl', 'wb') as f:
    pickle.dump(playerscores, f)
with open('playerstats.pkl', 'wb') as f:
    pickle.dump(playerelo, f)
with open('mapid.pkl', 'wb') as f:
    pickle.dump(maptoid, f)
with open('Lmaps.pkl', 'wb') as f:
        pickle.dump(maps, f)

with open('badges.pkl', 'wb') as f:
    pickle.dump(badges,f)


# Output:
# My New Google Sheets Spreadsheet
