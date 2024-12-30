# src/routes/tag_routes.py
from flask import Blueprint, request, jsonify, current_app, render_template
from src.firebase_manager import register_tag, fetch_tag

tag_routes = Blueprint("tag_routes", __name__)


@tag_routes.route("/register_tag/<uuid>", methods=["POST", "GET"])
def register_tag_route(uuid):
    """
    Registers a tag in Firestore if the tag doesn't already exist.

    Args:
        uuid (str): The UUID of the tag.

    Returns:
        A JSON response with the tag data and a 200 status code if the tag is registered successfully.
        If the tag already exists, returns a JSON response with an "error" key containing the error message and a 400 status code.
    """

    manager = current_app.manager
    tag = fetch_tag(
        uuid=uuid,
        manager=manager,
    )

    if request.method == "POST":
        data = request.json

        try:
            # Check if the tag already exists
            existing_tag = tag
            if existing_tag:
                return jsonify({"error": "Tag already exists!"}), 400

            # Register the tag
            register_tag(
                uuid=uuid,
                owner_name=data["owner_name"],
                owner_email=data["owner_email"],
                owner_phone=data["owner_phone"],
                manager=manager,
            )
            return jsonify({"message": "Tag registered successfully!"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    elif tag:
        return render_template("contact_owner.html", uuid=uuid)
    else:
        return render_template("register_tag.html", uuid=uuid)

# Get new route name for fetching tag after authenticated as owner
# @tag_routes.route("/fetch_tag/<uuid>", methods=["GET"])
# def fetch_tag_route(uuid):
#     """
#     Fetches a tag from Firestore using the provided UUID.

#     Args:
#         uuid (str): The UUID of the tag.

#     Returns:
#         A JSON response with the tag data and a 200 status code.
#         If the tag is not found, returns a JSON response with an "error" key containing the error message and a 404 status code.
#     """
#  
#    manager = current_app.manager

#     tag = fetch_tag(
#         uuid=uuid,
#         manager=manager,
#     )
#     if tag:
#         return jsonify(tag), 200
#     else:
#         return jsonify({"error": "Tag not found!"}), 404
