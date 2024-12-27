# src/routes/tag_routes.py
from flask import Blueprint, request, jsonify
from src.firebase_manager import register_tag

tag_routes = Blueprint("tag_routes", __name__)


@tag_routes.route("/register_tag/", methods=["POST"])
def register_tag_route():
    data = request.json
    try:
        register_tag(
            uuid=data["uuid"],
            owner_name=data["owner_name"],
            owner_email=data["owner_email"],
            owner_phone=data["owner_phone"],
        )
        return jsonify({"message": "Tag registered successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
