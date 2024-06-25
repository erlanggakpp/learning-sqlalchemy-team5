from flask import Blueprint, jsonify
import sys

sys.path.append("..") # Adds higher directory to python modules path.
from src.db import players

import copy

player_bp = Blueprint('players', __name__)

@player_bp.get("/")
def get_players():
    try:
        if len(players) == 0:
            raise Exception("There are no registered players yet")
        return jsonify({"players": players}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 200
    
@player_bp.get("/<int:id>")
def get_specific_player(id):
    try:
        target_player = None
        for player in players:
            if player["id"] == id:
                target_player = copy.deepcopy(player)
                break
        if target_player is None:
            raise Exception(f"There are no registered players with ID: {id}")
        return jsonify({"team": target_player}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400