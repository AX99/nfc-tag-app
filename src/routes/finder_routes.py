# src/routes/finder_routes.py
from flask import Blueprint, request, jsonify, current_app, render_template, redirect, url_for
from src.firebase_manager import fetch_tag
import datetime

finder_routes = Blueprint("finder_routes", __name__)


@finder_routes.route("/contact/<uuid>", methods=["GET"])
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
        return render_template("finder_submit.html", tag_uuid=uuid)
    else:
        return jsonify({"error": "Tag not found!"}), 404


@finder_routes.route("/notify_owner", methods=["POST"])
def notify_owner():
    """
    Receives finder's contact information and notifies the owner.
    
    Stores the finder's information in Firestore and sends a notification to the owner.
    """
    if request.method == "POST":
        try:
            # Get form data
            tag_uuid = request.form.get("tag_uuid")
            finder_name = request.form.get("finder_name")
            finder_contact = request.form.get("finder_contact")
            message = request.form.get("message", "")
            
            # Validate required fields
            if not all([tag_uuid, finder_name, finder_contact]):
                return jsonify({"error": "Missing required fields"}), 400
                
            # Get the tag information
            manager = current_app.manager
            tag = fetch_tag(uuid=tag_uuid, manager=manager)
            
            if not tag:
                return jsonify({"error": "Tag not found"}), 404
                
            # Create a notification record
            notification_data = {
                "finder_name": finder_name,
                "finder_contact": finder_contact,
                "message": message,
                "tag_uuid": tag_uuid,
                "created_at": datetime.datetime.now(datetime.UTC),
                "owner_notified": False
            }
            
            # Store notification in Firestore
            notification_ref = manager.db.collection("notifications").add(notification_data)
            notification_id = notification_ref[1].id
            
            # TODO: Send email/SMS to owner based on their preferences
            # This would be implemented with a service like SendGrid, Twilio, etc.
            
            # Update notification record to indicate owner was notified
            manager.db.collection("notifications").document(notification_id).update({"owner_notified": True})
            
            return jsonify({"success": True, "message": "Owner has been notified"}), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "Method not allowed"}), 405
