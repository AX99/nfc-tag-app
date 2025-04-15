# src/routes/tag_routes.py
from flask import (
    Blueprint,
    request,
    jsonify,
    current_app,
    render_template,
    redirect,
    url_for,
    flash,
)
from src.firebase_manager import register_tag, fetch_tag

tag_routes = Blueprint("tag_routes", __name__)


@tag_routes.route("/", methods=["GET"])
def index():
    return render_template("home.html")


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
        try:
            # Check if the tag already exists
            existing_tag = tag
            if existing_tag:
                flash("This tag is already registered!", "danger")
                return redirect(url_for("base_routes.tag_landing", uuid=uuid))

            # Check if the tag is authorized
            if not manager.is_authorized_tag(uuid):
                flash("This tag is not authorized. Please use a valid tag.", "danger")
                return redirect(url_for("base_routes.tag_landing", uuid=uuid))

            # Get form data
            owner_name = request.form.get("owner_name")
            owner_email = request.form.get("owner_email")
            owner_phone = request.form.get("owner_phone")

            # Validate required fields
            if not all([owner_name, owner_email, owner_phone]):
                flash("All fields are required.", "danger")
                return redirect(url_for("tag_routes.register_tag_route", uuid=uuid))

            # Register the tag
            success = register_tag(
                uuid=uuid,
                owner_name=owner_name,
                owner_email=owner_email,
                owner_phone=owner_phone,
                manager=manager,
            )

            if success:
                flash("Tag registered successfully!", "success")
                return redirect(url_for("base_routes.home"))
            else:
                flash("Failed to register tag. Please try again.", "danger")
                return redirect(url_for("tag_routes.register_tag_route", uuid=uuid))

        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for("tag_routes.register_tag_route", uuid=uuid))
    elif tag:
        return render_template("contact_owner.html", uuid=uuid)
    else:
        # Check if the tag is authorized before showing registration form
        is_authorized = manager.is_authorized_tag(uuid)
        return render_template(
            "register_form.html", uuid=uuid, is_authorized=is_authorized
        )
