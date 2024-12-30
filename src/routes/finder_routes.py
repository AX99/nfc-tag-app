# src/routes/finder_routes.py
from flask import Blueprint, request, jsonify, current_app
from src.firebase_manager import register_tag, fetch_tag

finder_routes = Blueprint("finder_routes", __name__)


@tag_routes.route("/contact/<uuid>", methods=["GET"])
def contact_owner_route(uuid):
    """
    Fetches a tag from Firestore using the provided UUID.

    Args:
        uuid (str): The UUID of the tag.

    Returns:
        A JSON response with the tag data and a 200 status code.
        If the tag is not found, returns a JSON response with an "error" key containing the error message and a 404 status code.
    """    
    manager = current_app.manager

    tag = fetch_tag(uuid=uuid, manager=manager)
    if tag:
        # logic to contact owner
        return jsonify(tag), 200
    else:
        return jsonify({"error": "Tag not found!"}), 404

