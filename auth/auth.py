from flask import Blueprint
from . import views

blueprint = Blueprint("auth", __name__, template_folder="templates")

# Login route
blueprint.add_url_rule('/authenticate', 'authenticate',
                       views.authenticate, methods=["GET", "POST"])
# Register route
blueprint.add_url_rule('/register', 'register',
                       views.register, methods=["GET", "POST"])
# Logout route
blueprint.add_url_rule('/endsession', 'endsession',
                       views.endsession, methods=["GET"])
