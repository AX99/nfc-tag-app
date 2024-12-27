from flask import Flask
from firebase_admin import firestore
from src.firebase_init.firebase_init import initialize_firebase
from src.routes.tag_routes import tag_routes

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase
db = initialize_firebase()

# Register Blueprint
app.register_blueprint(tag_routes, url_prefix="/api")

# Example usage
@app.route("/")
def home():
    return "Welcome to the NFC Contact System!"

if __name__ == "__main__":
    app.run(debug=True)
