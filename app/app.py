import os
from flask import Flask, jsonify
from .models import db, Player, Campaign
from .campaigns import get_active_campaigns
from .schemas import ma, player_schema, api_campaigns_schema
from .services import filter_eligible_campaigns

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "profiles.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB & Marshmallow
db.init_app(app)
ma.init_app(app)

# Healthcheck endpoint - usually on /healthcheck
@app.route('/', methods=['GET'])
def healthcheck():
    """Healthcheck endpoint"""
    return jsonify({"status": "ok"})


@app.route('/get_client_config/<player_id>', methods=['GET'])
def get_client_config(player_id):
    """API endpoint to get and update a player's profile with matching campaigns"""
    
    player = Player.query.filter_by(player_id=player_id).first()
    
    if not player:
        return jsonify({"error": "Player not found"}), 404
    
    # Mocked campaigns: deserialized for validation
    active_campaigns = api_campaigns_schema.load(get_active_campaigns())

    # Match campaigns with player profile
    matched_campaigns = [campaign for campaign in active_campaigns if filter_eligible_campaigns(player, campaign)]

    if matched_campaigns:
        campaigns = [Campaign(campaign_id=campaign['id'], name=campaign['name']) 
                for campaign in matched_campaigns]
        player.campaigns.extend(campaigns)
        db.session.commit()
    
    # Return updated player profile
    return jsonify(player_schema.dump(player))