# src/routes/base_routes.py
from flask import (
    Blueprint,
    render_template,
    current_app,
    request,
    flash,
    redirect,
    url_for,
)
from src.firebase_manager import fetch_tag

base_routes = Blueprint("base_routes", __name__)


@base_routes.route("/", methods=["GET"])
def home():
    """Render the home page."""
    return render_template("home.html")


@base_routes.route("/tag/<uuid>", methods=["GET"])
def tag_landing(uuid):
    """Landing page when a tag is scanned.

    This is the main entry point when someone scans an NFC tag.
    The UUID is extracted from the URL (which is programmed into the NFC tag).
    If the tag is registered, they'll be directed to the finder form.
    If not, they'll check if it's an authorized tag before showing the registration form.
    """
    manager = current_app.manager
    
    # First check if this tag is registered
    tag = fetch_tag(uuid, manager)
    
    if tag:
        # Tag exists - show finder form to contact owner
        return render_template("finder_submit.html", tag_uuid=uuid)
    else:
        # Tag doesn't exist - check if it's authorized before showing registration form
        is_authorized = manager.is_authorized_tag(uuid)
        return render_template(
            "register_form.html", 
            uuid=uuid,
            unregistered_tag=True,
            is_authorized=is_authorized
        )


@base_routes.route("/faq", methods=["GET"])
def faq():
    """Render the FAQ page."""
    return render_template("faq.html")


@base_routes.route("/privacy", methods=["GET"])
def privacy():
    """Render the privacy policy page."""
    return render_template("privacy.html")


@base_routes.route("/contact", methods=["GET", "POST"])
def contact():
    """Handle contact form submissions.

    GET: Display the contact form
    POST: Process the form submission (currently just logs to console)
    """
    if request.method == "POST":
        # For now, just print the contact form data to console
        # In production, you might send an email or store in database
        print("Contact form submission received:")
        print(f"Name: {request.form.get('name')}")
        print(f"Email: {request.form.get('email')}")
        print(f"Message: {request.form.get('message')}")
        print(f"Category: {request.form.get('category', 'General')}")

        # Flash a success message
        flash("Your message has been received. We'll get back to you soon!", "success")

        # Redirect to avoid form resubmission
        return redirect(url_for("base_routes.contact"))

    return render_template("contact.html")


@base_routes.route("/finder-confirmation", methods=["GET"])
def finder_confirmation():
    """Confirmation page after a finder submits their contact info."""
    return render_template("finder_confirmation.html")
