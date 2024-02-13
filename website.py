import pickle
from flask import Flask, render_template




with open('players.pkl', 'rb') as f:
    ranked_players = pickle.load(f)

with open('maps.pkl', 'rb') as f:
    maps = pickle.load(f)

with open('playermaps.pkl', 'rb') as f:
    playermaps = pickle.load(f)
with open('playerstats.pkl', 'rb') as f:
    playerelo = pickle.load(f)
with open('mapid.pkl', 'rb') as f:
    maptoid = pickle.load(f)
with open('Lmaps.pkl', 'rb') as f:
    Lmaps = pickle.load(f)
with open('badges.pkl', 'rb') as f:
    badges = pickle.load(f)
app = Flask(__name__, static_url_path='/static') 

playernames = list(playerelo.keys())
mapnames = list(maps.keys())

@app.route('/')
def index():

    total_maps = len(maps)   
    return render_template('index.html', players=ranked_players, total_maps = total_maps)

@app.route('/maps')
def mapss():
    return render_template('maps.html', maps=maps.items(), maptoid = maptoid)

@app.route('/maps/<int:map_id>')
def mapprofile(map_id):
    if 0 <= map_id <= len(maptoid):
        name = mapnames[map_id]
        victors = Lmaps.get(name, [])
        stars, rank, points, comps = maps[name]
        return render_template('mapprof.html', name=name, victors=victors, stars=stars, rank=rank, points=points,comps=comps)
    else:
        return "Map not found"


@app.route('/player/<int:player_id>')
def player(player_id):
    
    if 0 <= player_id < len(playernames):
        name = playernames[player_id]
        elo, completions, rank = playerelo[name]
        maps_completed = playermaps.get(name, [])
        total_maps = len(maps)
        return render_template('player.html', name=name, elo=elo, completions=completions, total_maps = total_maps, rank=rank, maps_completed=maps_completed, badges=badges)
    else:
        return "Player not found"

@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run(debug=True)
