import pickle
from flask import Flask, render_template, Blueprint
from flask_bootstrap import Bootstrap
import flask_login
from flask_login import current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required
from models.extensions import db, User
from auth import auth
blueprint = Blueprint("base", __name__, template_folder="templates")

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

class HomeView(AdminIndexView):
    """Admin view"""

    def is_accessible(self):
        """Checks that the user has administrator permissions"""
        try:
            # Returns true if user perms are 2, else false
            res = current_user.perms == 2
        except:
            # No perms, user is logged out
            res = False
        return res

    def inaccessible_callback(self, name, **kwargs):
        """
            Handle the response to inaccessible views.

            By default, it throw HTTP 403 error. 
            Now overidden to throw a HTTP 404 not found error.
            This is so that the website doesnt leak the admin route
        """
        return error_404("404")

app = Flask(__name__, static_url_path='/static') 
admin = Admin(app, base_template='layout.html',
              index_view=HomeView(name=' '), template_mode='bootstrap4')
login_manager = flask_login.LoginManager()
app.register_blueprint(auth.blueprint)
app.config["SECRET_KEY"] = "testsecrethihihihi"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
bootstrap = Bootstrap(app)
db.init_app(app)

playernames = list(playerelo.keys())    
mapnames = list(maps.keys())


class NEWModelView(ModelView):
    """Other admin pages"""

    def is_accessible(self):
        try:
            res = current_user.perms == 2
        except:
            res = False
        return res

    edit_template = 'editt.html'
    list_template = 'listt.html'
    create_template = 'creatt.html'

    
admin.add_view(NEWModelView(User, db.session))

login_manager.init_app(app)

login_manager.login_view = 'auth.authenticate'


@blueprint.app_errorhandler(404)
def error_404(error):
    """Returns a 404 error"""
    return render_template("error_404.html")

@login_manager.user_loader
def load_user(user_id):
    """Returns user given a userid"""
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():

    total_maps = len(maps)   
    return render_template('index.html', players=ranked_players, total_maps = total_maps)

@app.route('/maps')
def mapss():
    #return maps
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
@login_required
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
